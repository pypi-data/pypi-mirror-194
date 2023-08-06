#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#
import logging
from ._base import AnnotationParser, ParserType

__all__ = ['MotParser']
log = logging.getLogger(__name__)


class MotParser(AnnotationParser):
    """
    This parser is designed to parse the standard MOT_ multi object tracking dataset text files (https://arxiv.org/pdf/1906.04567.pdf).

    Keyword Args:
        class_label_map (list): list of class labels to translate a label to a class label index (the index in the list) and visa versa
        precision (integer, optional): The number of decimals for the coordinates; Default **None** (save as int)

    The MOT format contains all annotation from multiple video frames into one file.
    Each line of the file represents one bounding box from one image and is a spaces separated
    list of values structured as follows:

        <frame>,<id>,<bb_left>,<bb_top>,<bb_width>,<bb_height>,<valid>,<class_id>,<visibility>

    =========  ===========
    Name       Description
    =========  ===========
    frame      frame number that starts with 1 (integer)
    id         track id that starts with 1 (integer)
    bb_left    top left x coordinate of the bounding box (integer)
    bb_top     top left y coordinate of the bounding box (integer)
    bb_width   width of the bounding box (integer)
    bb_height  height of the bounding box (integer)
    valid      1 if the bounding box should be considered, 0 otherwise
    class_id   identifier of the object class starting with 1 (integer)
    visibility value between 0 and 1 that indicates how much of the object is visible (1 is fully visible, 0 is not visible)
    =========  ===========

    Note:
        The "valid" field is mapped to the "ignore" column and the "visibility" field to "occluded".

    Example:
        >>> gt.txt
            1,1,794.2,47.5,71.2,174.8,1,1,0.8
            1,2,164.1,19.6,66.5,163.2,1,1,0.5
            2,4,781.7,25.1,69.2,170.2,0,12,1.
    """
    parser_type = ParserType.MULTI_FILE
    serialize_group = 'video'
    extension = '.txt'

    def __init__(self, class_label_map=None, precision=None):
        super().__init__()

        self.add_column('video')
        self.add_column('frame')

        self.precision = precision
        self.class_label_map = class_label_map
        if self.class_label_map is None:
            raise ValueError('MOT annotation parser requires class_label_map argument')

    def pre_serialize(self, df):
        assert 'video' in df.columns, 'This parser requires a "video" column which contains the video names'
        assert 'frame' in df.columns, 'This parser requires a "frame" column which contains frame numbers'

        df['id'] = df['id'].fillna(-1)

        return df

    def serialize(self, df):
        result = ''
        for row in df.itertuples():
            class_index = self.class_label_map.index(row.class_label) + 1
            result += f'{row.frame},{row.id},{round(row.x_top_left, self.precision)},{round(row.y_top_left, self.precision)},{round(row.width, self.precision)},{round(row.height, self.precision)},{int(not row.ignore)},{class_index},{row.occluded}\n'

        return result

    def deserialize(self, rawdata, file_id=None):
        for line in rawdata.splitlines():
            elements = line.split(',')
            class_label = self.class_label_map[int(elements[7]) - 1]
            self.append(
                f'{file_id}--{elements[0]}',
                video=file_id,
                frame=int(elements[0]),
                class_label=class_label,
                id=int(float(elements[1])),
                x_top_left=float(elements[2]),
                y_top_left=float(elements[3]),
                width=float(elements[4]),
                height=float(elements[5]),
                ignore=not bool(int(elements[6])),
                occluded=float(elements[8]),
            )
