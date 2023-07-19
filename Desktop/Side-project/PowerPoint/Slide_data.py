import pandas as pd
import collections
import collections.abc
from pptx.util import Inches, Pt
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE


def read_pptx(file_path):

    content = {}

    # Load presentation
    prs = Presentation(file_path)

    # Loop through every slide
    for i, slide in enumerate(prs.slides):
        print(f"Slide {i + 1}:")
        # Loop through every shape in each slide

        # for placeholder in slide.slide_layout.placeholders:
        #     print(f"  Placeholder index: {placeholder.placeholder_format.idx}")
        #     print(f"  Placeholder type: {placeholder.placeholder_format.type}")
            # if placeholder.has_text_frame:
            #     # Loop through every paragraph in each shape
            #     for paragraph in placeholder.text_frame.paragraphs:
            #         print(paragraph.text)

        for shape in slide.shapes:

            # print(shape)
            print(shape.shape_type )
            if shape.shape_type == MSO_SHAPE_TYPE.PLACEHOLDER:
                print(f"Placeholder type: {shape.placeholder_format.type}")
                if shape.has_text_frame:
                    print(f"Text: {shape.text}")

            else:
                # print(f"Shape type: {shape.shape_type}")
                if shape.has_text_frame:
                    print(f"Text: {shape.text}")


def print_slide_contents(file_path):
    prs = Presentation(file_path)
    for i, slide in enumerate(prs.slides):

        print(f"Slide {i+1}:")
        for placeholder in slide.placeholders:
            print(placeholder.placeholder_format.idx)
            print(placeholder.placeholder_format.type)
            # Check if the placeholder is a title
            if placeholder.placeholder_format.idx == 0:
                print(f"  Title: {placeholder.text}")
            # Check if the placeholder is content
            elif placeholder.placeholder_format.idx == 1:
                print(f"  Content: {placeholder.text}")


print_slide_contents("PP_samples/sample.pptx")

# read_pptx("PP/sample.pptx")
