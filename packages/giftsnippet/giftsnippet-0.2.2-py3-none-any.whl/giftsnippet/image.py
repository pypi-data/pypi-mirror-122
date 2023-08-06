import base64


def get_data_uri_image(file, filetype='png'):
    with open(file, 'rb') as image:
        return transform_image_to_data_uri(image.read(), filetype)


def transform_image_to_data_uri(image, filetype='png', gift_escape=True):
    data_uri = 'data:image/' + filetype + ';base64,' + base64.b64encode(image).decode("utf-8")

    # : and = must be escaped inside the question content for gift and moodle import
    if gift_escape:
        data_uri = data_uri.replace(":", "\\:")
        data_uri = data_uri.replace("=", "\\=")

    return data_uri
