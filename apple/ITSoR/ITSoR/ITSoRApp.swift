//
//  ITSoRApp.swift
//  ITSoR
//
//  Created by Nathan McGuire on 2/27/26.
//

import SwiftUI

@main
struct ITSoRApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
#if os(macOS)
        .windowStyle(.hiddenTitleBar)
    .windowToolbarStyle(.unifiedCompact(showsTitle: false))
#endif
    }
}
