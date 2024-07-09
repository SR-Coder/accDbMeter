//
//  ContentView.swift
//  dbMeterIos
//
//  Created by Rob Dawson on 6/30/24.
//

import SwiftUI

struct ContentView: View {
    @StateObject var viewModel = DbMeterModel()
    var body: some View {
        VStack {
            //serverInput
            //label sending data?
            // toggle to send data
//            Image(systemName: "globe")
//                .imageScale(.large)
//                .foregroundStyle(.tint)
            Text("MQTT Server")
            TextField("Server", text: $viewModel.server)
            TextField("Your Device (shared with the server)", text: $viewModel.deviceName)
            
            Text("Db Level \(viewModel.lastPeak)")
            Toggle("Send Messages", isOn: $viewModel.sendMessages)
            
        }
        .padding()
    }
}

// sendData(boolean)

#Preview {
    ContentView()
}
