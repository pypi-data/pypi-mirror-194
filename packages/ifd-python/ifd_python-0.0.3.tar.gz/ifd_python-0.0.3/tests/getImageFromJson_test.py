from unittest import TestCase
from ifd.tools import getImageFromJson, getDictFromBytes
from ifd.entities import Image
import json

class getImageFromJson_test(TestCase):
    def test_image_load_with_json(self):

        json_image : bytes = b'''
        {
            "id": 1,
            "img_path": "/path/where/is/image",
            "img_checksum": "",
            "rotation": 0,
            "classification": {
                "score": 0.25636,
                "label": "TestLabel",
                "modele": {
                "label": "EfficientNetV2",
                "version": "V4"
                }
            },
            "detections": [
                {
                "score": 0.15688,
                "label": "PBO_TEST",
                "bbox": {
                    "xmin": 485,
                    "xmax": 125,
                    "ymin": 1256,
                    "ymax": 2562
                },
                "modele": {
                    "label": "YoloV5",
                    "version": "Detect-PBO"
                },
                "couleurs": [
                    {
                    "score": 0.5689,
                    "label": "VERT",
                    "bbox": {
                        "xmin": 523,
                        "xmax": 145,
                        "ymin": 1455,
                        "ymax": 1458
                    },
                    "modele": {
                        "label": "YoloV5",
                        "version": "Couleur-Smoove"
                    }
                    }
                ]
                }
            ],
            "ocr": {
                "score": 0.15688,
                "label": "PM_TEST",
                "bbox": {
                "xmin": 475,
                "xmax": 658,
                "ymin": 1452,
                "ymax": 1457
                },
                "modele": {
                "label": "YoloV5",
                "version": "v1-pto-s6"
                },
                "score_ocr": 0.5683,
                "label_ocr": "TF-1256-RE"
            },
            "ref_infra_pto": "TF-1256-RE"
        }
        '''

        data : dict = getDictFromBytes(json_image)
        image : Image = getImageFromJson(data)
        

        self.assertIs(image.id, data["id"])
        self.assertIs(image.img_path, data["img_path"])
        self.assertIs(image.img_checksum, data["img_checksum"])
        self.assertIs(image.rotation, data["rotation"])
        self.assertIs(image.ref_infra_pto, data["ref_infra_pto"])

        self.assertIs(image.detections[0].score, data["detections"][0]["score"])
        self.assertIs(image.detections[0].label, data["detections"][0]["label"])
        self.assertIs(image.detections[0].bbox.xmin, data["detections"][0]["bbox"]["xmin"])
        self.assertIs(image.detections[0].bbox.xmax, data["detections"][0]["bbox"]["xmax"])
        self.assertIs(image.detections[0].bbox.ymin, data["detections"][0]["bbox"]["ymin"])
        self.assertIs(image.detections[0].bbox.ymax, data["detections"][0]["bbox"]["ymax"])
        self.assertIs(image.detections[0].modele.label, data["detections"][0]["modele"]["label"])
        self.assertIs(image.detections[0].modele.version, data["detections"][0]["modele"]["version"])

        self.assertIs(image.detections[0].couleurs[0].score, data["detections"][0]["couleurs"][0]["score"])
        self.assertIs(image.detections[0].couleurs[0].label, data["detections"][0]["couleurs"][0]["label"])
        self.assertIs(image.detections[0].couleurs[0].bbox.xmin, data["detections"][0]["couleurs"][0]["bbox"]["xmin"])
        self.assertIs(image.detections[0].couleurs[0].bbox.xmax, data["detections"][0]["couleurs"][0]["bbox"]["xmax"])
        self.assertIs(image.detections[0].couleurs[0].bbox.ymin, data["detections"][0]["couleurs"][0]["bbox"]["ymin"])
        self.assertIs(image.detections[0].couleurs[0].bbox.ymax, data["detections"][0]["couleurs"][0]["bbox"]["ymax"])
        self.assertIs(image.detections[0].couleurs[0].modele.label, data["detections"][0]["couleurs"][0]["modele"]["label"])
        self.assertIs(image.detections[0].couleurs[0].modele.version, data["detections"][0]["couleurs"][0]["modele"]["version"])

        self.assertIs(image.detections[0].couleurs[0].label, data["detections"][0]["couleurs"][0]["label"])
        self.assertIs(image.detections[0].couleurs[0].label, data["detections"][0]["couleurs"][0]["label"])

        self.assertIs(image.ocr.score_ocr, data["ocr"]["score_ocr"])
        self.assertIs(image.ocr.label_ocr, data["ocr"]["label_ocr"])
        self.assertIs(image.ocr.score, data["ocr"]["score"])
        self.assertIs(image.ocr.label, data["ocr"]["label"])
        self.assertIs(image.ocr.bbox.xmin, data["ocr"]["bbox"]["xmin"])
        self.assertIs(image.ocr.bbox.xmax, data["ocr"]["bbox"]["xmax"])
        self.assertIs(image.ocr.bbox.ymin, data["ocr"]["bbox"]["ymin"])
        self.assertIs(image.ocr.bbox.ymax, data["ocr"]["bbox"]["ymax"])
        self.assertIs(image.ocr.modele.label, data["ocr"]["modele"]["label"])
        self.assertIs(image.ocr.modele.version, data["ocr"]["modele"]["version"])