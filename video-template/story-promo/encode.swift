import AVFoundation
import AppKit
let dir=CommandLine.arguments[1], out=CommandLine.arguments[2]
let files=try! FileManager.default.contentsOfDirectory(atPath:dir).filter{$0.hasSuffix(".jpg")}.sorted()
try? FileManager.default.removeItem(atPath:out)
let w=try! AVAssetWriter(outputURL:URL(fileURLWithPath:out),fileType:.mp4)
let inp=AVAssetWriterInput(mediaType:.video,outputSettings:[AVVideoCodecKey:AVVideoCodecType.h264,AVVideoWidthKey:1080,AVVideoHeightKey:1920,
 AVVideoCompressionPropertiesKey:[AVVideoAverageBitRateKey:14_000_000,AVVideoProfileLevelKey:AVVideoProfileLevelH264HighAutoLevel,AVVideoMaxKeyFrameIntervalKey:30]])
let ad=AVAssetWriterInputPixelBufferAdaptor(assetWriterInput:inp,sourcePixelBufferAttributes:[kCVPixelBufferPixelFormatTypeKey as String:kCVPixelFormatType_32ARGB,kCVPixelBufferWidthKey as String:1080,kCVPixelBufferHeightKey as String:1920])
w.add(inp);w.startWriting();w.startSession(atSourceTime:.zero)
for (i,f) in files.enumerated(){
  autoreleasepool{
    let img=NSImage(contentsOfFile:dir+"/"+f)!
    var cg=img.cgImage(forProposedRect:nil,context:nil,hints:nil)!
    var pb:CVPixelBuffer?;CVPixelBufferPoolCreatePixelBuffer(nil,ad.pixelBufferPool!,&pb)
    CVPixelBufferLockBaseAddress(pb!,[])
    let c=CGContext(data:CVPixelBufferGetBaseAddress(pb!),width:1080,height:1920,bitsPerComponent:8,bytesPerRow:CVPixelBufferGetBytesPerRow(pb!),space:CGColorSpace(name:CGColorSpace.sRGB)!,bitmapInfo:CGImageAlphaInfo.noneSkipFirst.rawValue)!
    c.draw(cg,in:CGRect(x:0,y:0,width:1080,height:1920))
    CVPixelBufferUnlockBaseAddress(pb!,[])
    while !inp.isReadyForMoreMediaData{usleep(2000)}
    ad.append(pb!,withPresentationTime:CMTime(value:Int64(i),timescale:30))
  }
}
inp.markAsFinished();let s=DispatchSemaphore(value:0);w.finishWriting{s.signal()};s.wait();print("done",files.count,w.status.rawValue)
