# 60 FPS Support - Feature Summary

## Overview
Added comprehensive 60 FPS support to the iPhone Webcam streaming application, enabling high frame rate video streaming from iPhone cameras to the virtual camera output.

## Changes Made

### 1. Server-Side Changes (main.py)
- **Virtual Camera FPS**: Updated `pyvirtualcam.Camera` initialization from 30 fps to 60 fps
- **Cross-platform Support**: Applied 60 fps setting to both Windows (with backend selection) and other platforms
- **Backend Compatibility**: Maintained compatibility with obs, unitycapture, and windows backends

### 2. Client-Side Changes (iphone.html)

#### Frame Rate Options
- **New 60 FPS Option**: Added 60 FPS as the top option in the Max FPS selector
- **Default Settings**: Changed default target FPS from 30 to 60 FPS
- **Adaptive Quality**: Adjusted initial quality settings for 60 FPS (0.6 vs 0.7 for lower FPS)

#### Camera Capabilities
- **Frame Rate Detection**: Added camera capability checking to determine maximum supported FPS
- **Automatic Adjustment**: System automatically adjusts requested FPS if camera doesn't support 60 FPS
- **Real-time Feedback**: Displays actual achieved frame rate in status messages

#### Performance Optimizations
- **Precise Timing**: Improved frame timing with 2ms tolerance for 60 FPS precision
- **Smart Frame Skipping**: Less aggressive frame skipping for high FPS (every 3rd vs every 2nd frame)
- **Processing Compensation**: Frame delays now account for processing time to maintain accurate timing
- **Adaptive Algorithm**: Enhanced network performance monitoring with more aggressive FPS reduction for poor connections

#### User Interface Enhancements
- **Performance Indicator**: Added efficiency percentage showing actual vs target FPS
- **Frame Drop Counter**: Real-time display of dropped frames
- **Adaptive FPS Display**: Shows current adaptive FPS setting
- **Camera Info**: Displays actual camera frame rate achieved during initialization

## Technical Implementation

### Frame Rate Management
```javascript
// Dynamic FPS adjustment based on network conditions
if (responseTime > 1000) {
    targetFPS = Math.max(10, targetFPS - 5);  // Aggressive reduction for 60fps
} else if (responseTime < 200) {
    targetFPS = Math.min(parseInt(maxFpsSelect.value), targetFPS + 2);
}
```

### Camera Constraints
```javascript
// Request high frame rate with capability checking
frameRate: { ideal: requestedFPS, max: maxSupportedFPS }
```

### Virtual Camera Output
```python
# 60 FPS virtual camera initialization
virtual_cam = pyvirtualcam.Camera(width=width, height=height, fps=60, backend=backend)
```

## Benefits

1. **Smoother Video**: 60 FPS provides significantly smoother video for applications requiring high frame rates
2. **Professional Quality**: Matches frame rates used in professional video production
3. **Gaming/Streaming**: Better suited for gaming streams and real-time applications
4. **Adaptive Performance**: Automatically adjusts based on network and device capabilities
5. **Backward Compatibility**: Still supports lower frame rates (10, 15, 24, 30 FPS)

## Usage Instructions

1. **Select 60 FPS**: Choose "60 FPS" from the Max FPS dropdown
2. **Camera Compatibility**: The system will automatically check if your iPhone camera supports 60 FPS
3. **Monitor Performance**: Watch the efficiency percentage and adaptive FPS indicators
4. **Network Optimization**: The system will automatically reduce FPS if network conditions are poor

## System Requirements

- **iPhone**: Modern iPhone with 60 FPS camera support (iPhone 6s and newer)
- **Network**: Stable network connection for high data throughput
- **Virtual Camera**: OBS Studio or compatible virtual camera software
- **Processing Power**: Sufficient CPU for encoding/decoding 60 FPS video streams

## Troubleshooting

- **Low Efficiency**: If efficiency is below 80%, consider reducing resolution or quality
- **High Frame Drops**: Check network connection and reduce quality settings
- **Camera Not Supporting 60 FPS**: Older devices may automatically fall back to 30 FPS
- **Virtual Camera Issues**: Ensure OBS Studio virtual camera is started before streaming

## Future Enhancements

- **120 FPS Support**: Potential support for 120 FPS on supported devices
- **Variable Frame Rate**: Dynamic frame rate adjustment based on scene complexity
- **Hardware Acceleration**: GPU-based encoding for better performance
- **Quality Presets**: Pre-configured quality profiles for different use cases