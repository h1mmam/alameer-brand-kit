import AVFoundation
let v=URL(fileURLWithPath:CommandLine.arguments[1]),a=URL(fileURLWithPath:CommandLine.arguments[2]),o=URL(fileURLWithPath:CommandLine.arguments[3])
try? FileManager.default.removeItem(at:o)
let comp=AVMutableComposition()
let va=AVURLAsset(url:v),aa=AVURLAsset(url:a)
let vt=va.tracks(withMediaType:.video)[0],at=aa.tracks(withMediaType:.audio)[0]
let ct=comp.addMutableTrack(withMediaType:.video,preferredTrackID:kCMPersistentTrackID_Invalid)!
try! ct.insertTimeRange(CMTimeRange(start:.zero,duration:va.duration),of:vt,at:.zero)
let ca=comp.addMutableTrack(withMediaType:.audio,preferredTrackID:kCMPersistentTrackID_Invalid)!
try! ca.insertTimeRange(CMTimeRange(start:.zero,duration:min(aa.duration,va.duration)),of:at,at:.zero)
let ex=AVAssetExportSession(asset:comp,presetName:AVAssetExportPresetHighestQuality)!
ex.outputURL = o; ex.outputFileType = .mp4
let s=DispatchSemaphore(value:0);ex.exportAsynchronously{s.signal()};s.wait()
print(ex.status.rawValue,ex.error?.localizedDescription ?? "ok")
