# iPhone Webcam - Network Efficiency Guide

## Network Optimizations Implemented

### 1. Adaptive Quality Control
- **Automatic Quality Adjustment**: The app monitors network latency and automatically adjusts image quality
- **Dynamic Compression**: JPEG/WebP compression levels adjust based on network performance
- **Resolution Scaling**: For very poor connections, resolution is temporarily reduced

### 2. Smart Frame Rate Management
- **Adaptive FPS**: Target frame rate reduces during high latency periods
- **Frame Skipping**: Intelligently skips frames when network is struggling
- **Manual FPS Control**: Users can set maximum FPS (10-30 FPS)

### 3. Connection Optimization
- **Keep-Alive Connections**: HTTP connections are reused to reduce overhead
- **Request Timeouts**: 5-second timeout prevents hanging connections
- **Exponential Backoff**: Failed requests retry with increasing delays

### 4. Data Compression
- **Image Optimization**: Better JPEG/WebP compression with adaptive quality
- **Gzip Support**: Server supports compressed data transmission
- **Frame Size Limits**: Maximum 1MB frame size to prevent network overload

## Performance Monitoring

The interface now displays:
- **Current FPS**: Actual frames per second achieved
- **Target FPS**: Current target based on network conditions
- **Latency**: Round-trip time for frame uploads
- **Frame Size**: Current compressed frame size in KB
- **Quality**: Current compression quality percentage
- **Drop Count**: Number of failed frame transmissions

## Usage Tips for Different Network Conditions

### High-Speed WiFi (>50 Mbps)
- Use **High Quality (0.8)** setting
- Set **30 FPS** for smooth streaming
- **4K resolution** if your device supports it

### Standard WiFi (10-50 Mbps)
- Use **Medium Quality (0.7)** setting (default)
- Set **24-30 FPS**
- **1280x720** resolution recommended

### Slow WiFi/Mobile Data (<10 Mbps)
- Use **Low Quality (0.5)** or **Auto (Adaptive)**
- Set **10-15 FPS**
- **640x360** resolution
- Enable automatic quality adjustment

### Very Poor Connection
- Use **Auto (Adaptive)** quality
- Set **10 FPS** maximum
- **640x360** or lower resolution
- The app will automatically reduce quality and resolution as needed

## Automatic Optimizations

When **Auto (Adaptive)** quality is selected:
- **Good connection** (<200ms latency): Gradually increases quality and FPS
- **Poor connection** (>1000ms latency): Reduces quality, FPS, and compression
- **Very poor connection** (>2000ms latency): Temporarily reduces resolution
- **Connection recovers**: Automatically restores original resolution

## Technical Details

### Frame Processing Pipeline
1. Capture video frame from camera
2. Apply rotation if needed (portrait to landscape)
3. Resize to target resolution
4. Compress with adaptive quality
5. Monitor upload time and adjust settings
6. Skip frames if network is struggling

### Quality Metrics
- **Latency monitoring**: Tracks round-trip time for each frame
- **Frame drop tracking**: Counts failed transmissions
- **Adaptive thresholds**: Quality adjusts based on performance history
- **Recovery logic**: Gradually improves quality when connection stabilizes

### Server Optimizations
- **Threaded Flask server**: Handles multiple concurrent requests
- **Frame size validation**: Rejects oversized frames
- **Compression support**: Accepts gzipped data
- **CORS optimization**: Minimal headers for faster processing

## Troubleshooting

### If streaming is slow or choppy:
1. Check your WiFi signal strength
2. Try **Auto (Adaptive)** quality setting
3. Reduce FPS to 15 or 10
4. Lower resolution to 640x360
5. Close other bandwidth-heavy applications

### If frames are dropping frequently:
1. Enable **Auto (Adaptive)** quality
2. Set FPS to 10
3. Use lowest resolution setting
4. Check the latency display - should be <500ms for stable streaming

### For optimal performance:
1. Use 5GHz WiFi when available
2. Position close to WiFi router
3. Close unnecessary browser tabs
4. Enable **Auto (Adaptive)** quality for best balance