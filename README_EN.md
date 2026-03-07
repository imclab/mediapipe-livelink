[简体中文](README.md)

# mediapipe-livelink

Face and motion capture using mediapipe, send data to Unreal Engine with livelink

## Project structure

- `src/main.cpp`: main executable entry. Opens camera/video frames with OpenCV, runs MediaPipe detection, and sends encoded blendshape packets over UDP.
- `src/test.cpp`: alternate executable for experimenting with a different MediaPipe graph and callback style.
- `include/mediapipe/*.h`: C++ interface boundary to an external MediaPipe implementation (`CreateMediapipeInterface`).
- `include/livelink/*.hpp`: Live Link domain logic:
  - `blend_shape_config.hpp`: enum of Unreal face blendshapes + smoothing helper.
  - `live_link_base.hpp`: common geometry helpers and base class.
  - `face_live_link.hpp`: mapping from MediaPipe landmarks to blendshape weights and binary packet encoding.
- `blend_shape_config.json`: index/threshold tuning used by `FaceLiveLink` during expression estimation.
- `LiveLink.md`: notes about packet layout and byte-level protocol fields.
- `include/asio` and `include/nlohmann`: vendored third-party headers.

## Runtime data flow

1. Capture frame from camera.
2. Convert BGR to RGB and pass frame to MediaPipe.
3. Receive landmarks callback from MediaPipe graph.
4. Convert landmarks to blendshape weights with `FaceLiveLink`.
5. Encode weights into a Live Link packet.
6. Send packet to Unreal Live Link endpoint via UDP (default `127.0.0.1:11111`).

## Important implementation notes

- Blendshape estimation here is heuristic and threshold-driven (from `blend_shape_config.json`), not ML-regressed.
- Smoothing is handled per blendshape using a fixed-size deque mean (`SmoothDeque`).
- Packet encoding writes binary values into a `std::vector<char>` with optional byte reversal for network order.
- Build paths in `CMakeLists.txt` are currently Windows-local absolute paths and may need adjustment on another machine.

## TODO

- [x] Face Capture

    Calculation using [3D](https://google.github.io/mediapipe/solutions/face_mesh.html#face-transform-module) coordinates.
    
    Learn from [MeFaMo](https://github.com/JimWest/MeFaMo) to calculate the BlendShape weight.

- [ ] It is not an ideal solution to calculate the BlendShape by mathematically setting the weight manually. A better solution is to build a model to return the output of the mediapipe (or the output of other facial recognition models) to the BlendShape weight. At present, there is no character picture and corresponding BlendShape data set.

- [ ] Motion capture

## LICENSE

- [asio](THIRD_LICENSE/asio/LICENSE)

- [nlohmann](THIRD_LICENSE/nlohmann/LICENSE)

- [MeFaMo](THIRD_LICENSE/MeFaMo/LICENSE)
