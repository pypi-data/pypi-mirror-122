import math
import json
import concurrent.futures

import requests
import boto3
import cv2
import numpy as np


textract_client = boto3.client('textract')


def rotate_image(image, angle):
    h, w = image.shape[:2]
    img_c = (w / 2, h / 2)

    rot = cv2.getRotationMatrix2D(img_c, angle, 1)

    rad = math.radians(angle)
    sin = math.sin(rad)
    cos = math.cos(rad)
    b_w = int((h * abs(sin)) + (w * abs(cos)))
    b_h = int((h * abs(cos)) + (w * abs(sin)))

    rot[0, 2] += ((b_w / 2) - img_c[0])
    rot[1, 2] += ((b_h / 2) - img_c[1])

    rotated_image = cv2.warpAffine(image, rot, (b_w, b_h), flags=cv2.INTER_LINEAR)
    return rotated_image


def rotate_point(matrix, point, translate=(0, 0)):
    return (matrix[0][0] * point[0] + matrix[0][1] * point[1] + translate[0],
            matrix[1][0] * point[0] + matrix[1][1] * point[1] + translate[1])


def get_angle_from_textract_lines(image, textract_response):
    angles = []
    height, width = image.shape[:2]
    for block in textract_response["Blocks"]:
        if block["BlockType"] != "LINE":
            continue
        polygon = block["Geometry"]["Polygon"]
        v = np.array([polygon[1]["X"] * width - polygon[0]["X"] * width,
                      polygon[1]["Y"] * height - polygon[0]["Y"] * height])
        v /= np.linalg.norm(v)
        angles.append(math.atan2(-v[1], v[0]))

    return np.average(angles)


def rotate_textract_lines(image, textract_response, angle):
    height, width = image.shape[:2]

    rotation_matrix = [
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)]
    ]

    corner_points_transformed = []
    for corner_point in (0, 0), (width, 0), (0, height), (width, height):
        corner_points_transformed.append(rotate_point(rotation_matrix, corner_point))
    min_x = min(corner_point[0] for corner_point in corner_points_transformed)
    min_y = min(corner_point[1] for corner_point in corner_points_transformed)
    max_x = max(corner_point[0] for corner_point in corner_points_transformed)
    max_y = max(corner_point[1] for corner_point in corner_points_transformed)

    rotated_height, rotated_width = int(max_y - min_y), int(max_x - min_x)

    translation = (-min_x if min_x < 0 else 0, -min_y if min_y < 0 else 0)

    for block in textract_response["Blocks"]:
        polygon = block["Geometry"]["Polygon"]
        transformed_polygon = []
        for point_idx, point in enumerate(polygon):
            x, y = point["X"] * width, point["Y"] * height
            x_transformed, y_transformed = rotate_point(rotation_matrix, (x, y), translation)
            y_transformed /= rotated_height
            x_transformed /= rotated_width
            transformed_polygon.append({"X": x_transformed, "Y": y_transformed})
        poly_min_x = min(point["X"] for point in transformed_polygon)
        poly_min_y = min(point["Y"] for point in transformed_polygon)
        poly_max_x = max(point["X"] for point in transformed_polygon)
        poly_max_y = max(point["Y"] for point in transformed_polygon)
        block["Geometry"]["Polygon"] = transformed_polygon
        block["Geometry"]["BoundingBox"] = {"Left": poly_min_x, "Top": poly_min_y,
                                            "Width": poly_max_x - poly_min_x,
                                            "Height": poly_max_y - poly_min_y}


def deskew_based_on_textract_lines(image, textract_response):
    angle = get_angle_from_textract_lines(image, textract_response)
    rotate_textract_lines(image, textract_response, angle)
    rotated_image = rotate_image(image, -np.degrees(angle))
    return angle, rotated_image


def run_textract_on_image(page_image):
    page_image_bgr = cv2.cvtColor(page_image, cv2.COLOR_RGB2BGR)
    _, encoded_image = cv2.imencode(".jpg", page_image_bgr, [cv2.IMWRITE_JPEG_QUALITY, 80])
    image_bytes = encoded_image.tobytes()
    return textract_client.detect_document_text(Document={'Bytes': image_bytes})


def prefix_textract_ids(textract_response, prefix):
    for block in textract_response["Blocks"]:
        block["Id"] = prefix + block["Id"]
        for relation in block.get("Relationships", []):
            relation["Ids"] = [prefix + id_ for id_ in relation["Ids"]]


def convert_textract_response(textract_response, translation, ratio):
    for block in textract_response["Blocks"]:
        block["Geometry"]["BoundingBox"]["Top"] = (block["Geometry"]["BoundingBox"]["Top"] + translation) * ratio
        block["Geometry"]["BoundingBox"]["Height"] *= ratio
        for point in block["Geometry"]["Polygon"]:
            point["Y"] = (point["Y"] + translation) * ratio


def convert_bottom_textract_response(textract_response, split_ratio):
    translation = (1.0 - split_ratio) / split_ratio
    ratio = 1.0 / (translation + 1.0)
    convert_textract_response(textract_response, translation, ratio)


def convert_top_textract_response(textract_response, split_ratio):
    translation = (1.0 - split_ratio) / split_ratio
    ratio = 1.0 / (translation + 1.0)
    convert_textract_response(textract_response, translation=0.0, ratio=ratio)


def get_image_bounding_box(textract_block, image):
    height, width = image.shape[:2]
    x_min = textract_block["Geometry"]["BoundingBox"]["Left"] * width
    y_min = textract_block["Geometry"]["BoundingBox"]["Top"] * height
    x_max = (textract_block["Geometry"]["BoundingBox"]["Left"] +
             textract_block["Geometry"]["BoundingBox"]["Width"]) * width
    y_max = (textract_block["Geometry"]["BoundingBox"]["Top"] +
             textract_block["Geometry"]["BoundingBox"]["Height"]) * height
    return int(round(x_min)), int(round(y_min)), int(round(x_max)), int(round(y_max))


def bbox_area(bbox):
    return (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])


def bbox_intersection(bbox1, bbox2):
    return (max(bbox1[0], bbox2[0]),
            max(bbox1[1], bbox2[1]),
            min(bbox1[2], bbox2[2]),
            min(bbox1[3], bbox2[3]))


def mostly_covers(bbox_covering, bbox_covered, min_ratio=0.85):
    covered_area = bbox_area(bbox_covered)
    intersection = bbox_intersection(bbox_covering, bbox_covered)
    intersection_area = bbox_area(intersection)
    return bool(intersection_area > covered_area * min_ratio)


def merge_textract_results(top_textract_response, bottom_textract_response, image: np.ndarray, split_ratio: float):
    top_angle = get_angle_from_textract_lines(image, top_textract_response)
    bottom_angle = get_angle_from_textract_lines(image, top_textract_response)
    #  there is something wrong the image should already be deskewed
    if abs(top_angle) > 0.5 or bottom_angle > 0.5:
        return None

    prefix_textract_ids(top_textract_response, prefix="0#")
    prefix_textract_ids(bottom_textract_response, prefix="1#")
    convert_top_textract_response(top_textract_response, split_ratio=split_ratio)
    convert_bottom_textract_response(bottom_textract_response, split_ratio=split_ratio)

    block_by_id = {block["Id"]: block for block in top_textract_response["Blocks"] + bottom_textract_response["Blocks"]}

    top_lines = [block for block in top_textract_response["Blocks"] if block["BlockType"] == "LINE"]
    line_field = np.full(image.shape[:2], -1, dtype=int)
    merged_lines = []
    top_lines_bounding_box = []
    for line_idx, top_line in enumerate(top_lines):
        min_x, min_y, max_x, max_y = get_image_bounding_box(top_line, image)
        top_lines_bounding_box.append((min_x, min_y, max_x, max_y))
        line_field[min_y:max_y, min_x:max_x] = line_idx
        merged_lines.append(top_line)

    lines_to_delete = set()
    bottom_lines = [block for block in bottom_textract_response["Blocks"] if block["BlockType"] == "LINE"]
    for bottom_line in bottom_lines:
        min_x, min_y, max_x, max_y = get_image_bounding_box(bottom_line, image)
        bottom_bounding_box = (min_x, min_y, max_x, max_y)
        replaces = False
        discard = False
        intersecting_lines = np.unique(line_field[min_y:max_y, min_x:max_x])
        for intersecting_line_idx in sorted(intersecting_lines):
            if intersecting_line_idx == -1:
                continue

            if mostly_covers(top_lines_bounding_box[intersecting_line_idx], bottom_bounding_box):
                discard = True
                break

            if mostly_covers(bottom_bounding_box, top_lines_bounding_box[intersecting_line_idx]):
                if replaces:
                    lines_to_delete.add(intersecting_line_idx)
                else:
                    merged_lines[intersecting_line_idx] = bottom_line
                    replaces = True

        if not (replaces or discard):
            merged_lines.append(bottom_line)

    merged_lines = [line for line_idx, line in enumerate(merged_lines) if line_idx not in lines_to_delete]

    word_blocks = []
    for line_block in merged_lines:
        for relation in line_block.get("Relationships", []):
            if relation["Type"] != "CHILD":
                continue
            for child_block_id in relation["Ids"]:
                word_blocks.append(block_by_id[child_block_id])

    top_textract_response["Blocks"] = merged_lines + word_blocks

    return top_textract_response


def split_page_and_run_textract(page_image: np.ndarray, split_ratio: float = 0.6):
    height, width = page_image.shape[:2]
    split_height = int(round(split_ratio * height))
    top_half = page_image[:split_height]
    bottom_half = page_image[-split_height:]

    textract_executor = concurrent.futures.ThreadPoolExecutor(2)
    top_task = textract_executor.submit(run_textract_on_image, top_half)
    bottom_task = textract_executor.submit(run_textract_on_image, bottom_half)

    top_result = top_task.result()
    bottom_result = bottom_task.result()

    return merge_textract_results(top_result, bottom_result, page_image, split_ratio)


def visualize_textract_output(image, textract_output):
    new_image = np.array(image)
    for block in textract_output["Blocks"]:
        if block["BlockType"] != "LINE":
            continue
        left, top, right, bottom = get_image_bounding_box(block, image)
        new_image = cv2.rectangle(new_image, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), 3)
    return new_image


def should_split_page(page_image, textract_response):
    if page_image.shape[0] > 4000:
        return True
    min_height = min([block["Geometry"]["BoundingBox"]["Height"] for block in textract_response["Blocks"]])
    if min_height < 0.01:
        return True
    return False


def run_textract(image_bytes):
    textract_response = textract_client.detect_document_text(Document={'Bytes': image_bytes})
    image_np_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_np_array, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    rotation_angle = get_angle_from_textract_lines(image, textract_response)
    if abs(np.degrees(rotation_angle)) > 0.5:
        rotate_textract_lines(image, textract_response, rotation_angle)
        image = rotate_image(image, -np.degrees(rotation_angle))
    else:
        rotation_angle = 0.0

    if should_split_page(image, textract_response):
        textract_response = split_page_and_run_textract(image)

    textract_response["Rotation"] = np.degrees(rotation_angle)

    return textract_response


def run_newspaper_segmentation_on_image(image_bytes, api_key):
    upload_url_response = requests.get("https://api.arcanum.com/v1/newspaper-segmentation/upload-url",
                                       headers={"x-api-key": api_key}).json()
    requests.put(upload_url_response["url"], data=image_bytes)

    textract_response = run_textract(image_bytes)

    response = requests.get("https://api.arcanum.com/v1/newspaper-segmentation/analyze-page",
                            data=json.dumps(
                                {"image": upload_url_response["key"], "textract_response": textract_response}),
                            headers={"x-api-key": api_key})

    return response.json()


def run_newspaper_segmentation(image_path, api_key):
    with open(image_path, "rb") as input_image:
        image_bytes = input_image.read()

    return run_newspaper_segmentation_on_image(image_bytes, api_key)
