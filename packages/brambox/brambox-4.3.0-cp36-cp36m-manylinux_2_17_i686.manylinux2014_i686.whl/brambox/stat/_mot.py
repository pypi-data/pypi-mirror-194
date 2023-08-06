#
#   Copyright EAVISE
#   Author: Tanguy Ophoff
#
#   Functions for generating Multi Object Tracking Statistics
#
import logging
import numpy as np
from scipy.optimize import linear_sum_assignment
from ..util import np_col, DualGroupByNumpy
from ._matchboxes import match_det
from . import coordinates

__all__ = ['mota', 'idf1']
log = logging.getLogger(__name__)


def mota(det, anno, threshold=0.5, ignore=None):
    """
    Computes the MOTA score between a detection and annotation dataframe set.
    This function will match detections and annotations by computing the IoU and then look at the 'id' column to compute ID Switches.

    Args:
        det (pandas.DataFrame): Dataframe with detections
        anno (pandas.DataFrame): Dataframe with annotations
        threshold (number): Threshold to count a detection as true positive; Default **0.5**
        ignore (boolean, optional): Whether to consider the ignore flag of annotations when matching detections; Default **True**

    Returns:
        Number: MOTA score between 0 and 1.

    Warning:
        The dataframes need to have an additional "frame" column which contains the numerical index of the image frame in the video.
        This allows the function to know in which order to process the images to compute ID switches.

        If your dataset comprises of multiple different videos,
        you should add an additional "video" column that allows the function to group the detections by video for the computations.

    Note:
        If `ignore` is true, this function will match the detections using :func:`~brambox.stat.coordinates.pdollar`
        and consider ignored annotations as regions that can be matched to multiple times,
        otherwise it will use a regular :func:`~brambox.stat.coordinates.iou` and discard the ignored labels.
        If there are no ignored annotations, this boils down to the same. |br|
        By default (`ignore == None`), this function will check whether there are ignored annotations and set the ignore value accordingly.

        If you want more control over the parameters to match detections (eg. Change the criteria to something else than IoU),
        you can call the :func:`brambox.stat.match_det` function and provide other arguments. |br|
        This function will first check whether the detection dataframe has tp/fp columns and compute them otherwise.

    Note:
        The detection confidence is disregarded in this function, as is most often the case.
        This is because usually you would choose a working point when deploying a detection+tracking setup. |br|
        If you do need to compute MOTA at different thresholds, you should run this function with various filtered dataframes:

        >>> det = bb.io.load(...)
        >>> anno = bb.io.load(...)
        >>> for conf in range(100, 10):
        ...     filtered_det = det[det['confidence'] >= conf / 100]
        ...     print(mota(filtered_det, anno))
    """
    assert 'frame' in det.columns, 'DataFrames need to have a numerical "frame" column'
    has_video = 'video' in det.columns
    if ignore is None:
        ignore = anno['ignore'].any()

    # Match Detections and Annotations
    if not {'tp', 'fp'}.issubset(det.columns):
        crit = coordinates.pdollar if ignore else coordinates.iou
        label = len({*det['class_label'].unique(), *anno['class_label'].unique()}) > 1
        det = match_det(det, anno, threshold, criteria=crit, class_label=label, ignore=2 if ignore else 0)

    # Get Annotation ID
    columns = ['annotation', 'id', 'video', 'frame'] if has_video else ['annotation', 'id', 'frame']
    pos_matches = det.loc[det['tp'], columns].copy()
    pos_matches['annotation'] = anno.loc[pos_matches['annotation'].values, 'id'].values
    pos_matches = pos_matches.sort_values('frame')

    # ID switches
    ids = 0
    groups = pos_matches.groupby('video') if has_video else [(None, pos_matches)]
    for _, group in groups:
        id_pairs = {}
        for row in group.itertuples():
            prev_id = id_pairs.get(row.annotation, row.id)
            id_pairs[row.annotation] = row.id
            if prev_id != row.id:
                ids += 1

    # FN/FP
    num_gt = (~anno.ignore).sum() if ignore else len(anno.index)
    tp = len(pos_matches.index)
    fp = det['fp'].sum()
    fn = num_gt - tp

    # Compute MOTA
    return 1 - ((fn + fp + ids) / num_gt)


def idf1(det, anno, threshold=0.5, criteria=coordinates.iou, class_label=True, **kwargs):
    """
    Computes the IDF1 score between a detection and annotation dataframe set.
    This function will match detections and annotations and then look at the 'id' column to compute the best track ID matches.

    Args:
        det (pandas.DataFrame): Dataframe with detections
        anno (pandas.DataFrame): Dataframe with annotations
        threshold (number): Threshold to count a detection as true positive; Default **0.5**
        criteria (callable, optional): function to compute a criteria value between detection and annotation (eg. IoU); Default :func:`brambox.stat.coordinates.pdollar`
        class_label (boolean, optional): Whether class_labels must be equal to be able to match annotations and detections; Default **True**
        **kwargs (dict, optional): Extra keyword arguments that are passed on to the *criteria* function

    Returns:
        Number: IDF1 score between 0 and 1.

    Warning:
        If your dataframe contains data from multiple videos, make sure to not reuse any ID number !
        Each ID number should be unique to that specific tracked object.

    Note:
        The IDF1 metric tries to find the optimal match between detection and annotation IDs,
        such that the IDs coincide for a maximum number of frames. |br|
        As such, it is not really possible to take "ignored" annotation into consideration and they are thus regarded as regular annotations.

    Note:
        The detection confidence is disregarded in this function, as is most often the case.
        This is because usually you would choose a working point when deploying a detection+tracking setup. |br|
        If you do need to compute IDF1 at different thresholds, you should run this function with various filtered dataframes:

        >>> det = bb.io.load(...)
        >>> anno = bb.io.load(...)
        >>> for conf in range(100, 10):
        ...     filtered_det = det[det['confidence'] >= conf / 100]
        ...     print(idf1(filtered_det, anno))
    """
    if det.image.dtype.name == 'category' and anno.image.dtype.name == 'category' and set(det.image.cat.categories) != set(anno.image.cat.categories):
        log.error('Annotation and detection dataframes do not have the same image categories')

    # Create copies
    det = det.copy()
    anno = anno.copy()

    # Convert class label to integer category
    if class_label:
        anno_cl = anno['class_label']
        det_cl = det['class_label']
        _, cl_keys = np.unique(np.concatenate([anno_cl, det_cl]), return_inverse=True)
        cl_keys = np.split(cl_keys, anno_cl.shape)
        anno['class_key'] = cl_keys[0]
        det['class_key'] = cl_keys[1]

    # Rename IDs to be strictly increasing numbers
    # This part is basically the same as `det['id'] = det['id'].replace({...})`
    # but implemented with a lookup array in NumPy as it is ~100x faster
    det_id = np_col(det, 'id')
    uniq_id = np.unique(det_id)
    id_map = np.empty(uniq_id.max() + 1, dtype=int)
    id_map[uniq_id] = np.arange(len(uniq_id))
    det['id'] = id_map[det_id]

    anno_id = np_col(anno, 'id')
    uniq_id = np.unique(anno_id)
    id_map = np.empty(uniq_id.max() + 1, dtype=int)
    id_map[uniq_id] = np.arange(len(uniq_id))
    anno['id'] = id_map[anno_id]

    # Sum of Binary Overlap Matrices
    def sum_binary_overlap_matrices(g1, g2):
        nonlocal B, criteria, threshold, class_label, kwargs

        # Compute binary overlap
        binary_overlap = np.asarray(criteria(g1, g2, **kwargs)) >= threshold
        if class_label:
            binary_overlap &= g1['class_key'][:, None] == g2['class_key'][None, :]

        # Add overlap to result array
        B[g1['id'][:, None], g2['id'][None, :]] += binary_overlap

    B = np.zeros((anno['id'].nunique(), det['id'].nunique()), dtype=int)
    DualGroupByNumpy(anno, det, 'image').apply_none(sum_binary_overlap_matrices)

    # Linear Sum Assignment (Best ID match)
    rows, cols = linear_sum_assignment(B, maximize=True)
    lsa = B[rows, cols].sum()

    # IDF1
    return lsa / (0.5 * (len(det.index) + len(anno.index)))
