#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#
import logging
from ._base import DetectionParser, ParserType

__all__ = ['MotParser']
log = logging.getLogger(__name__)


class MotParser(DetectionParser):
    """
    This parser is designed to parse the standard MOT_ multi object tracking dataset detection files (https://arxiv.org/pdf/1906.04567.pdf).

    Keyword Args:
        class_label (str, optional): Class label for the detections; Default **""**
        precision (integer, optional): The number of decimals for the coordinates; Default **None** (save as int)

    The MOT format contains all detections from a single video into one file.
    Each line of the file represents one bounding box from one image and is a spaces separated
    list of values structured as follows:

        <frame>,<id>,<bb_left>,<bb_top>,<bb_width>,<bb_height>,<confidence>,<world_x>,<world_y>,<world_z>

    ==========  ===========
    Name        Description
    ==========  ===========
    frame       frame number that starts with 1 (integer)
    id          track id that starts with 1 (integer)
    bb_left     top left x coordinate of the bounding box (integer)
    bb_top      top left y coordinate of the bounding box (integer)
    bb_width    width of the bounding box (integer)
    bb_height   height of the bounding box (integer)
    confidence  detection confidence of the model (float)
    world_x     World X coordinate (set to -1 for 2D detection and tracking)
    world_y     World Y coordinate (set to -1 for 2D detection and tracking)
    world_z     World Z coordinate (set to -1 for 2D detection and tracking)
    ==========  ===========

    Warning:
        This format does not store label information and can thus only be used for single class detection (and tracking).

    Note:
        The world coordinates are not used in brambox and will thus be set to **-1**.

    Example:
        >>> MOT20-01.txt
            1,1,562.295,402.922,87.734,199.537,0.926,-1,-1,-1
            1,2,308.310,331.108,85.444,170.464,0.917,-1,-1,-1
            1,3,167.468,789.383,110.514,235.149,0.912,-1,-1,-1
            1,4,1049.593,646.272,106.097,193.428,0.903,-1,-1,-1
            1,5,860.305,572.673,75.274,187.385,0.903,-1,-1,-1
    """
    parser_type = ParserType.MULTI_FILE
    serialize_group = 'video'
    extension = '.txt'

    def __init__(self, class_label='', precision=None):
        super().__init__()

        self.precision = precision

        self.add_column('video')
        self.add_column('frame')
        self.add_column('class_label', class_label)

    def pre_serialize(self, df):
        assert 'video' in df.columns, 'This parser requires a "video" column which contains the video names'
        assert 'frame' in df.columns, 'This parser requires a "frame" column which contains frame numbers'

        df['id'] = df['id'].fillna(-1)

        return df

    def serialize(self, df):
        result = ''
        for row in df.itertuples():
            result += f'{row.frame},{row.id},{round(row.x_top_left, self.precision)},{round(row.y_top_left, self.precision)},{round(row.width, self.precision)},{round(row.height, self.precision)},{row.confidence},-1,-1,-1\n'

        return result

    def deserialize(self, rawdata, file_id=None):
        for line in rawdata.splitlines():
            elements = line.split(',')
            self.append(
                f'{file_id}--{elements[0]}',
                video=file_id,
                frame=int(elements[0]),
                id=int(float(elements[1])),
                x_top_left=float(elements[2]),
                y_top_left=float(elements[3]),
                width=float(elements[4]),
                height=float(elements[5]),
                confidence=float(elements[6]),
            )
