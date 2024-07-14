//
//  DbMeterModel.swift
//  dbMeterIos
//
//  Created by Rob Dawson on 7/8/24.
//

import CoreLocation
import Foundation
import AVFoundation
import CocoaMQTT


//https://medium.com/@meet237/displaying-current-location-on-map-using-cllocationmanager-and-mapkit-in-swiftui-f42ea94391ed
final class DbMeterModel: NSObject, ObservableObject, CLLocationManagerDelegate {
    
    
    @Published var lastAverage: Float?
    @Published var lastPeak: Float = 0.0
    @Published var port: UInt16 = 1885
    @Published var lastMessage: String=""
    var mqtt5: CocoaMQTT5?;

    @Published public var server: String = "10.0.0.213"
    @Published public var deviceName: String = ""

    @Published public var sendMessages = false {
        didSet {
            if sendMessages {
                let clientID = "CocoaMQTT-" + UIDevice.current.identifierForVendor!.uuidString
                mqtt5 = CocoaMQTT5(clientID: clientID, host: server, port: port)
                let connectProperties = MqttConnectProperties()
                connectProperties.topicAliasMaximum = 0
                connectProperties.sessionExpiryInterval = 0
                connectProperties.receiveMaximum = 100
                connectProperties.maximumPacketSize = 500
                mqtt5!.connectProperties = connectProperties
//                mqtt5!.username = "test"
//                mqtt5!.password = "public"
                mqtt5!.willMessage = CocoaMQTT5Message(topic: "offline", string: "dieout")
                mqtt5!.keepAlive = 60
//                mqtt5!.delegate = self
                var result = mqtt5!.connect()
                if !result {
                    print("Had a connection failure, so retrying")
                    result = mqtt5!.connect()
                }
                print("mqtt connection status is: \(result)")
                
            } else {
                if mqtt5 != nil {
                    mqtt5?.disconnect();
                }
            }
        }
    }


    var timer: DispatchSourceTimer?

    override init() {
        super.init()
        print("Init of DbMeterModel")
        guard let url = directoryURL() else {
            print("Unable to find a init directoryURL")
            return
        }
        
        let recordSettings = [
            AVSampleRateKey: 8000,
            AVFormatIDKey : NSNumber(value: Int32(kAudioFormatLinearPCM) as Int32),
            AVNumberOfChannelsKey: 2,
            AVLinearPCMBitDepthKey: 8,
            AVLinearPCMIsFloatKey: true,
            AVSampleRateConverterAudioQualityKey: AVAudioQuality.high.rawValue
        ] as [String : Any]
        let audioSession = AVAudioSession.sharedInstance()
        do {
            print("starting")
            let locationManager = CLLocationManager.init()
            locationManager.delegate=self
            locationManager.requestWhenInUseAuthorization()
            locationManager.desiredAccuracy = kCLLocationAccuracyBestForNavigation
            locationManager.distanceFilter = kCLDistanceFilterNone
            locationManager.startUpdatingLocation()

            try audioSession.setCategory(AVAudioSession.Category.record)
            let audioRecorder = try AVAudioRecorder(url: url, settings: recordSettings)
            audioRecorder.prepareToRecord()
            audioRecorder.record()
            try audioSession.setActive(true)
            audioRecorder.isMeteringEnabled = true
            recordForever(audioRecorder: audioRecorder, locationManager: locationManager)
        } catch let err {
            print("Unable start recording", err)
        }
    }

    func directoryURL() -> URL? {
        let fileManager = FileManager.default
        let urls = fileManager.urls(for: .documentDirectory, in: .userDomainMask)
        let documentDirectory = urls[0] as URL
        let soundURL = documentDirectory.appendingPathComponent("sound.m4a")
        return soundURL
    }
    
    func locationManager(_ manager: CLLocationManager, didUpdateLocations locations: [CLLocation])
    {
    
    }
    
    func locationManager(_ manager: CLLocationManager, didFailWithError error: any Error)
    {
        print("Failed with error: \(error)")
        
    }
    
    /**
     Format dBFS to dB
     THIS GIVES WRONG NUMBERS!!
     https://stackoverflow.com/questions/38246919/how-to-detect-max-db-swift
     - author: RÅGE_Devil_Jåmeson
     - date: (2016-07-13) 20:07:03
     
     - parameter dBFSValue: raw value of averagePowerOfChannel
     
     - returns: formatted value
     */
    func dBFS_convertTo_dB (dBFSValue: Float) -> Float
    {
        var level:Float = 0.0
        let peak_bottom:Float = -60.0 // dBFS -> -160..0   so it can be -80 or -60
        
        if dBFSValue < peak_bottom
        {
            level = 0.0
        }
        else if dBFSValue >= 0.0
        {
            level = 1.0
        }
        else
        {
            let root:Float              =   2.0
            let minAmp:Float            =   powf(10.0, 0.05 * peak_bottom)
            let inverseAmpRange:Float   =   1.0 / (1.0 - minAmp)
            let amp:Float               =   powf(10.0, 0.05 * dBFSValue)
            let adjAmp:Float            =   (amp - minAmp) * inverseAmpRange
            
            level = powf(adjAmp, 1.0 / root)
        }
        return level
    }
    
    func recordDatapoint(average: Float, peak: Float, location: CLLocation?) {
        // Send a single datapoint to DataDog
        let timestamp = Date().timeIntervalSince1970 * 1000
        let datapointPayload = [
            "timestamp": timestamp,
            "sensorName": deviceName,
            "sensorId":String(ProcessInfo().processIdentifier),
            "latitude": location?.coordinate.latitude as Any,
            "longitude": location?.coordinate.longitude as Any,
            "dbLevel":calcDb(power: peak),
          
        ] as [String : Any]
        DispatchQueue.main.async {
            self.lastAverage = self.calcDb(power: average)
            self.lastPeak = self.calcDb(power: peak)
        }
        sendMessage(message: datapointPayload)

    }
    
    func sendMessage(message: [String: Any]) {
        guard let mqttPayload = try? JSONSerialization.data(withJSONObject: message, options: []) else {
            print("Bad URL or body")
            return
        }
        let publishProperties = MqttPublishProperties()
        print("Will send request:", String(decoding: mqttPayload, as: UTF8.self))

       publishProperties.contentType = "JSON"
       let publishResult = mqtt5!.publish("DBMeter", withString: String(decoding: mqttPayload, as: UTF8.self), qos: .qos1, properties: publishProperties)
        
//        publish(_ topic: String, withString string: String, qos: CocoaMQTTQoS = .qos1, DUP: Bool =
    }
    
    func calcDb(power: Float) -> Float
    {
                
        let adjustedPower = power + 155 - 50
                
        var dB:Float = 0.0
        if adjustedPower < 0.0 {
            dB = 0
        } else if adjustedPower < 40.0 {
            dB = adjustedPower * 0.875
        } else if adjustedPower < 100.0 {
            dB = adjustedPower - 15
        } else if adjustedPower < 110.0 {
            dB = adjustedPower * 2.5 - 165
        } else {
            dB = 110
        }
        return dB;
    }

    func recordForever(audioRecorder: AVAudioRecorder, locationManager: CLLocationManager) {
        let queue = DispatchQueue(label: "io.segment.decibel", attributes: .concurrent)
        timer = DispatchSource.makeTimerSource(flags: [], queue: queue)
        timer?.schedule(deadline: .now(), repeating: .milliseconds(500), leeway: .milliseconds(100))
        timer?.setEventHandler { [ self] in
            audioRecorder.updateMeters()
            locationManager.requestLocation()
            // NOTE: seems to be the approx correction to get real decibels
            let average = audioRecorder.averagePower(forChannel: 0)
            let peak = audioRecorder.peakPower(forChannel: 0)
            if sendMessages {
                self.recordDatapoint(average: average, peak: peak, location: locationManager.location)
            }
        }
        timer?.resume()
    }
    
    
}

