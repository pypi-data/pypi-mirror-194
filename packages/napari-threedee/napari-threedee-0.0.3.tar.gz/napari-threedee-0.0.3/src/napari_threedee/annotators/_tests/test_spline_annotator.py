from napari.layers import Points

from napari_threedee.annotators.spline_annotator import SplineAnnotator


def test_spline_annotator_instantiation(make_napari_viewer, blobs_layer_4d_plane):
    viewer = make_napari_viewer(ndisplay=3)
    plane_layer = viewer.add_layer(blobs_layer_4d_plane)
    annotator = SplineAnnotator(
        viewer=viewer,
        image_layer=plane_layer,
    )
    assert isinstance(annotator.points_layer, Points)
    assert annotator.SPLINE_ID_FEATURES_KEY in annotator.points_layer.features
    assert len(annotator.points_layer.data) == 0


def test_add_point(spline_annotator):
    points_layer = spline_annotator.points_layer
    label = spline_annotator.SPLINE_ID_FEATURES_KEY

    # start empty
    assert len(points_layer.data) == 0

    # add points, make sure filament id in feature table matches the annotator
    points_layer.add([1, 2, 3, 4])
    assert len(points_layer.data) == 1
    assert points_layer.features[label][0] == spline_annotator.active_spline_id

    # change filemanet_id in annotator, add point, check matches
    spline_annotator.active_spline_id = 534
    points_layer.add([2, 3, 4, 5])
    assert points_layer.features[label][1] == spline_annotator.active_spline_id


def test_get_colors(spline_annotator):
    """Test getting spline colors from the annotator."""
    points_layer = spline_annotator.points_layer
    spline_annotator.active_spline_id = 0
    points_layer.add([1, 2, 3, 4])
    spline_annotator.active_spline_id = 1
    points_layer.add([2, 3, 4, 5])

    spline_colors = spline_annotator._get_spline_colors()
    for spline_id in (0, 1):
        assert spline_id in spline_colors
