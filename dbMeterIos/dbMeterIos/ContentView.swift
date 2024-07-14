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
            Form {
                //serverInput
                //label sending data?
                // toggle to send data
                //            Image(systemName: "globe")
                //                .imageScale(.large)
                //                .foregroundStyle(.tint)
                Text("DB Meter iOS Client").font(.title)
                Section {
                    LabeledContent {
                        TextField("Server", text: $viewModel.server).fontWeight(.bold)
                    } label: {Text("Server")}
                    LabeledContent {
                        TextField("Device", text: $viewModel.deviceName).fontWeight(.bold)
                    } label: {Text("Device")}
                    Toggle("Monitoring Enabled", isOn: $viewModel.sendMessages)
                } header : {
                    Text("Settings")
                }
                
                Section {
                    LabeledContent("Peak Level", value: "\(viewModel.lastPeak)")
                    LabeledContent("Average Level", value: "\(viewModel.lastAverage)")
                } header:  {
                    Text("state")
                }
        }
        .padding()
    }
}

// sendData(boolean)

#Preview {
    ContentView()
}
