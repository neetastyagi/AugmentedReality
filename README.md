# Augmented Reality

## Summary

This repository contains an implementation and helper scripts for an Augmented Reality (AR) assignment (CS6476 Problem Set 3). The code demonstrates marker detection, homography estimation and image projection (warping) to insert one image/video into another image/video using perspective transforms.

NOTE: The repository does not include the input images and input videos used for producing results. To run the scripts and tests you must provide your own images and videos in the expected folders (see "Inputs" below).

## Files

- ps3.py
  - Main implementation for the assignment.
  - Includes functions to:
    - find_markers(image, template): template-based marker detection (uses template matching, some rotation and noise-handling heuristics).
    - draw_box(image, markers, thickness): draw a rectangular box connecting marker points.
    - find_four_point_transform(src_points, dst_points): compute 3x3 homography using linear algebra / SVD (custom implementation — does not use cv2.getPerspectiveTransform or cv2.findHomography).
    - apply_homography(src, H): apply a homography to a set of points.
    - project_imageA_onto_imageB(imageA, imageB, homography): projects imageA into the marked area of imageB using the provided homography (pixel-wise inverse mapping implementation).
    - video_frame_generator(filename): generator that yields frames from a video (uses cv2.VideoCapture and yields None at end).
    - find_aruco_markers(image, aruco_dict): wrapper to detect ArUco markers using cv2.aruco and return ordered corner coordinates and IDs.
    - find_aruco_center(markers, ids): compute centers of detected ArUco markers (averages corner coordinates).
  - Some small helper functions and utilities (ordering points, averaging coordinates, distance/angle helpers) are also present.
  - Note: a few trivial helper functions (e.g. euclidean_distance) are present but raise NotImplementedError — the primary functionality needed for the assignment is implemented in this module.

- ps3_harris.py
  - An alternate/experimental implementation that focuses on Harris corner detection to locate markers.
  - Contains a Harris-based find_markers implementation and utilities for grouping corner detections into four marker positions.
  - Several functions are left as NotImplemented (for example project_imageA_onto_imageB, find_four_point_transform, and others) — this module appears to be a partially completed or alternate approach to ps3.py.

- ps3_tests.py
  - Unit tests used to validate the required behavior for the assignment.
  - Tests included for:
    - get_corners_list (expected list of four image corners),
    - find_markers on several synthetic and wall images,
    - find_four_point_transform (checks homography shape, dtype and correctness by comparing warped corners),
    - project_imageA_onto_imageB (compares SSIM between the implemented projection and cv2.warpPerspective output).
  - Run with: python -m unittest ps3_tests.py (or python ps3_tests.py)

- experiment.py
  - Driver script with helper routines to run each part of the assignment and to generate output images/videos for manual inspection.
  - Contains helpers for parts 1–7, including:
    - helper_for_part_4_and_5 / helper_for_part_6 / helper_for_part_7
    - mp4_video_writer, save_image, mark_location
  - Reads images from `input_images/` and videos from `input_videos/` and writes outputs to the working directory (OUT_DIR).
  - Useful as an end-to-end runner to visualize marker detection and projection results.

## Inputs (NOT included)

This repository references input images and videos but those files are NOT included in the repository. You must provide them locally for the code to run. Expected directories and some example filenames used in the scripts/tests:

- input_images/
  - template.jpg (template used for template matching)
  - img-3-a-1.png (advert image used in example projection)
  - my-image.png (example image used in experiment part 7)
  - test_images/ (used by tests, e.g. simple_rectangle.png, rectangle_wall.png, etc.)

- input_videos/
  - ps3-4-a.mp4, ps3-4-b.mp4, ps3-4-c.mp4, ps3-4-d.mp4 (example videos referenced in experiment.py)
  - my-ad.mp4 (your own ad/video used in part 6)
  - ps3-7.mp4 (video with ArUco markers used in part 7)

If you try to run experiment.py or the tests without adding these files, the code will fail when attempting to open missing files (cv2.imread will return None or VideoCapture will not open). Place your input images and videos in the directories above or modify the scripts to point to your own file locations.

## Dependencies

- Python 3.x
- numpy
- opencv (cv2) — recommended package: opencv-python
- scipy (for ndimage.rotate used in some matching routines)

Install with pip if needed:

pip install numpy opencv-python scipy

## How to run

- Run tests:
  - python -m unittest ps3_tests.py

- Run the experiment driver to generate outputs (after adding input files):
  - python experiment.py
  - Modify which parts are called in the __main__ section of experiment.py by commenting/uncommenting part_* calls.

## Notes and Caveats

- The repository intentionally does not include the input images and videos. If you need the original data used by the assignment, add them to the input_images/ and input_videos/ directories or contact the instructor/source that provided the assignment materials.

- Some modules (ps3_harris.py) are partial/experimental. The primary, more complete implementation is in ps3.py.

- The project contains both handcrafted implementations (SVD-based homography solver, pixel-wise inverse mapping projection) and OpenCV utilities (ArUco detection). Tests in ps3_tests.py expect numerical accuracy (SSIM and coordinate tolerance) — small implementation differences can affect the test results.


