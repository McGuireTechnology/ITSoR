//
//  ContentView.swift
//  ITSoR
//
//  Created by Nathan McGuire on 2/27/26.
//

import SwiftUI
import Combine

struct ContentView: View {
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass

    @StateObject private var viewModel = BladeViewModel()
    @State private var showingCreateForm = false
    @State private var showingConnectionSheet = false
    @State private var splitVisibility: NavigationSplitViewVisibility = .all
    @State private var favoriteResources: [AppResource] = [.tenants, .users]
    @State private var recentResources: [AppResource] = []

    var body: some View {
        ZStack {
            LinearGradient(
                colors: [ITSoRBrand.appBackgroundTop, ITSoRBrand.appBackgroundBottom],
                startPoint: .top,
                endPoint: .bottom
            )
            .ignoresSafeArea()

            VStack(spacing: 0) {
                BrandTopBarView(
                    searchText: $viewModel.searchText,
                    searchResults: viewModel.globalSearchResults,
                    activeTenantName: viewModel.activeTenantName,
                    favorites: favoriteResources,
                    recents: recentResources,
                    tenantOptions: viewModel.tenantMenuOptions,
                    onSelectResource: { resource in
                        selectResource(resource)
                    },
                    onToggleFavorite: { resource in
                        toggleFavorite(resource)
                    },
                    onSelectTenant: { tenantID in
                        viewModel.selectTenantFromMenu(id: tenantID)
                    },
                    onSubmitSearch: {
                        viewModel.submitGlobalSearch()
                    },
                    onActivateSearchResult: { result in
                        viewModel.activateGlobalSearchResult(result)
                    },
                    onOpenConnection: {
                        showingConnectionSheet = true
                    },
                    onSignOut: {
                        viewModel.signOut()
                        showingConnectionSheet = true
                    }
                )
#if os(macOS)
                .ignoresSafeArea(.container, edges: .top)
                .zIndex(2)
#endif

                NavigationSplitView(columnVisibility: $splitVisibility) {
                    DomainResourceBladeView(
                        selectedDomain: $viewModel.selectedDomain,
                        selectedResource: $viewModel.selectedResource,
                        resources: viewModel.resourcesForSelectedDomain
                    )
                    .navigationSplitViewColumnWidth(min: 250, ideal: 300, max: 360)
                } detail: {
                    AdaptiveWorkspaceView(
                        title: viewModel.listBladeTitle,
                        items: viewModel.listItems,
                        selectedItemID: $viewModel.selectedItemID,
                        isLoading: viewModel.isLoading,
                        selectedResource: viewModel.selectedResource,
                        selectedTenant: viewModel.selectedTenant,
                        editName: $viewModel.editName,
                        onList: { Task { await viewModel.listSelectedResource() } },
                        onCreate: {
                            if viewModel.selectedResource == .tenants {
                                showingCreateForm = true
                            }
                        },
                        onConnect: {
                            showingConnectionSheet = true
                        },
                        onRead: { Task { await viewModel.readSelectedTenant() } },
                        onUpdate: { Task { await viewModel.updateSelectedTenant() } },
                        onReplace: { Task { await viewModel.replaceSelectedTenant() } },
                        onDelete: { Task { await viewModel.deleteSelectedTenant() } }
                    )
                }
                .tint(ITSoRBrand.purple)
            }
        }
        .fontDesign(.monospaced)
        .preferredColorScheme(.light)
#if os(macOS)
        .toolbarVisibility(.visible, for: .windowToolbar)
        .toolbar(removing: .sidebarToggle)
#endif
        .sheet(isPresented: $showingCreateForm) {
            CreateTenantView { draft in
                Task { await viewModel.createTenant(from: draft) }
            }
#if os(iOS)
            .presentationDetents([.medium, .large])
            .presentationDragIndicator(.visible)
#endif
        }
        .sheet(isPresented: $showingConnectionSheet) {
            ConnectionView(
                serverURL: $viewModel.serverURLText,
                identifier: $viewModel.identifier,
                signupUsername: $viewModel.signupUsername,
                signupEmail: $viewModel.signupEmail,
                password: $viewModel.password,
                onLogin: { Task { await viewModel.login() } },
                onSignup: { Task { await viewModel.signup() } }
            )
#if os(iOS)
            .presentationDetents([.large])
            .presentationDragIndicator(.visible)
#endif
        }
        .overlay(alignment: .bottom) {
            if let status = viewModel.statusMessage {
                Text(status)
                    .font(.footnote)
                    .padding(.horizontal, 14)
                    .padding(.vertical, 8)
                    .background(.ultraThinMaterial, in: Capsule())
                    .overlay(
                        Capsule()
                            .stroke(ITSoRBrand.deepBlue.opacity(0.14), lineWidth: 1)
                    )
                    .padding(.bottom, 10)
            }
        }
        .task {
            updateSplitVisibility()
            await viewModel.ensureDefaultSelection()
        }
        .onChange(of: horizontalSizeClass) { _, _ in
            updateSplitVisibility()
        }
        .onChange(of: viewModel.selectedDomain) { _, _ in
            viewModel.handleDomainChanged()
        }
        .onChange(of: viewModel.selectedResource) { previousValue, currentValue in
            viewModel.handleResourceChanged(from: previousValue, to: currentValue)
            if let selectedResource = viewModel.selectedResource {
                trackRecent(resource: selectedResource)
            }
        }
    }

    private func updateSplitVisibility() {
#if os(iOS)
        splitVisibility = horizontalSizeClass == .compact ? .automatic : .all
#else
        splitVisibility = .all
#endif
    }

    private func selectResource(_ resource: AppResource) {
        viewModel.selectedDomain = .platform
        viewModel.selectedResource = resource
    }

    private func toggleFavorite(_ resource: AppResource) {
        if let existingIndex = favoriteResources.firstIndex(of: resource) {
            favoriteResources.remove(at: existingIndex)
            viewModel.statusMessage = "Removed \(resource.title) from favorites"
        } else {
            favoriteResources.append(resource)
            viewModel.statusMessage = "Added \(resource.title) to favorites"
        }
    }

    private func trackRecent(resource: AppResource) {
        recentResources.removeAll(where: { $0 == resource })
        recentResources.insert(resource, at: 0)
        if recentResources.count > 6 {
            recentResources = Array(recentResources.prefix(6))
        }
    }
}

private struct BrandTopBarView: View {
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass

    @Binding var searchText: String
    let searchResults: [TopBarSearchResult]
    let activeTenantName: String
    let favorites: [AppResource]
    let recents: [AppResource]
    let tenantOptions: [Tenant]
    let onSelectResource: (AppResource) -> Void
    let onToggleFavorite: (AppResource) -> Void
    let onSelectTenant: (String?) -> Void
    let onSubmitSearch: () -> Void
    let onActivateSearchResult: (TopBarSearchResult) -> Void
    let onOpenConnection: () -> Void
    let onSignOut: () -> Void

    private var isCompactBar: Bool {
        horizontalSizeClass == .compact
    }

    private var leadingPadding: CGFloat {
#if os(macOS)
        78
#else
        isCompactBar ? 10 : 12
#endif
    }

    private var trailingPadding: CGFloat {
        isCompactBar ? 10 : 12
    }

    private var topPadding: CGFloat {
#if os(macOS)
        6
#else
        isCompactBar ? 7 : 8
#endif
    }

    private var bottomPadding: CGFloat {
        isCompactBar ? 7 : 8
    }

    var body: some View {
        HStack(spacing: isCompactBar ? 8 : 10) {
            HStack(spacing: 6) {
                appDrawerMenu
                favoritesMenu
                recentsMenu
            }

            brandBlock

            Spacer(minLength: isCompactBar ? 8 : 14)

            searchBar

            Spacer(minLength: isCompactBar ? 8 : 14)

            HStack(spacing: 6) {
                adminMenu
                tenantMenu
                userMenu
            }
        }
        .padding(.leading, leadingPadding)
        .padding(.trailing, trailingPadding)
        .padding(.top, topPadding)
        .padding(.bottom, bottomPadding)
        .background(
            LinearGradient(
                colors: [ITSoRBrand.deepBlue, ITSoRBrand.purple, ITSoRBrand.hotPink],
                startPoint: .leading,
                endPoint: .trailing
            )
        )
        .overlay(alignment: .bottom) {
            Rectangle()
                .fill(Color.white.opacity(0.2))
                .frame(height: 1)
        }
        .shadow(color: ITSoRBrand.deepBlue.opacity(0.22), radius: 8, y: 3)
    }

    private var brandBlock: some View {
        HStack(spacing: isCompactBar ? 6 : 8) {
            ITSoRCubeLogoView()
                .frame(width: isCompactBar ? 22 : 28, height: isCompactBar ? 22 : 28)

            VStack(alignment: .leading, spacing: 1) {
                Text("IT-SoR")
                    .font(.system(size: isCompactBar ? 13 : 15, weight: .bold, design: .monospaced))
                    .foregroundStyle(.white)
                    .lineLimit(1)

                if !isCompactBar {
                    Text("IT System of Record")
                        .font(.system(size: 11, weight: .regular, design: .monospaced))
                        .foregroundStyle(.white.opacity(0.8))
                        .lineLimit(1)
                }
            }
        }
    }

    private var searchBar: some View {
        HStack(spacing: 6) {
            Image(systemName: "magnifyingglass")
                .font(.system(size: 12, weight: .semibold))
                .foregroundStyle(Color.white.opacity(0.85))

            TextField("Search current list", text: $searchText)
                .textFieldStyle(.plain)
                .font(.system(size: isCompactBar ? 12 : 13, weight: .regular, design: .monospaced))
                .foregroundStyle(.white)
                .onSubmit {
                    onSubmitSearch()
                }
#if os(iOS)
                .textInputAutocapitalization(.never)
                .autocorrectionDisabled(true)
#endif

            if !searchResults.isEmpty {
                Menu {
                    ForEach(searchResults) { result in
                        Button {
                            onActivateSearchResult(result)
                        } label: {
                            Label(result.title, systemImage: result.iconName)
                        }
                    }
                } label: {
                    Image(systemName: "list.bullet")
                        .font(.system(size: 12, weight: .semibold))
                        .foregroundStyle(Color.white.opacity(0.9))
                }
                .buttonStyle(.plain)
            }

            if !searchText.isEmpty {
                Button {
                    searchText = ""
                } label: {
                    Image(systemName: "xmark.circle.fill")
                        .font(.system(size: 12, weight: .regular))
                        .foregroundStyle(Color.white.opacity(0.85))
                }
                .buttonStyle(.plain)
            }
        }
        .padding(.horizontal, 10)
        .padding(.vertical, 6)
        .frame(maxWidth: isCompactBar ? 210 : 440)
        .background(
            RoundedRectangle(cornerRadius: 8, style: .continuous)
                .fill(Color.white.opacity(0.17))
        )
        .overlay(
            RoundedRectangle(cornerRadius: 8, style: .continuous)
                .stroke(Color.white.opacity(0.26), lineWidth: 1)
        )
    }

    private var appDrawerMenu: some View {
        Menu {
            Section("App Drawer") {
                ForEach(AppResource.allCases) { resource in
                    Button {
                        onSelectResource(resource)
                    } label: {
                        Label(resource.title, systemImage: resource.iconName)
                    }
                }
            }
        } label: {
            topBarMenuLabel(title: "Apps", systemImage: "square.grid.2x2")
        }
    }

    private var favoritesMenu: some View {
        Menu {
            Section("Favorites") {
                if favorites.isEmpty {
                    Text("No favorites yet")
                } else {
                    ForEach(favorites) { resource in
                        Button {
                            onSelectResource(resource)
                        } label: {
                            Label(resource.title, systemImage: resource.iconName)
                        }
                    }
                }
            }

            Section("Manage Favorites") {
                ForEach(AppResource.allCases) { resource in
                    Button {
                        onToggleFavorite(resource)
                    } label: {
                        Label(
                            favorites.contains(resource) ? "Remove \(resource.title)" : "Add \(resource.title)",
                            systemImage: favorites.contains(resource) ? "star.slash" : "star"
                        )
                    }
                }
            }
        } label: {
            topBarMenuLabel(title: "Favorites", systemImage: "star")
        }
    }

    private var recentsMenu: some View {
        Menu {
            Section("Recents") {
                if recents.isEmpty {
                    Text("No recent resources")
                } else {
                    ForEach(recents) { resource in
                        Button {
                            onSelectResource(resource)
                        } label: {
                            Label(resource.title, systemImage: resource.iconName)
                        }
                    }
                }
            }
        } label: {
            topBarMenuLabel(title: "Recents", systemImage: "clock.arrow.circlepath")
        }
    }

    private var adminMenu: some View {
        Menu {
            Button("Admin Dashboard") { onSelectResource(.tenants) }
            Button("Authorization") { onSelectResource(.roles) }
            Button("System Settings") { onOpenConnection() }
        } label: {
            topBarMenuLabel(title: "Admin", systemImage: "gearshape")
        }
    }

    private var tenantMenu: some View {
        Menu {
            Button("All Tenants") {
                onSelectTenant(nil)
            }

            if tenantOptions.isEmpty {
                Text("No tenants loaded")
            } else {
                ForEach(tenantOptions) { tenant in
                    Button(tenant.name) {
                        onSelectTenant(tenant.id)
                    }
                }
            }
        } label: {
            topBarTenantLabel
        }
    }

    private var userMenu: some View {
        Menu {
            Button("Profile") { onSelectResource(.users) }
            Button("Preferences") { onOpenConnection() }
            Divider()
            Button("Sign Out") { onSignOut() }
        } label: {
            topBarMenuLabel(title: "User", systemImage: "person.crop.circle")
        }
    }

    private var topBarTenantLabel: some View {
        HStack(spacing: 4) {
            Image(systemName: "building.2")
                .font(.system(size: 11, weight: .semibold))
            if !isCompactBar {
                Text(activeTenantName)
                    .lineLimit(1)
            }
        }
        .font(.system(size: 11, weight: .semibold, design: .monospaced))
        .foregroundStyle(Color.white.opacity(0.95))
        .padding(.horizontal, 8)
        .padding(.vertical, 5)
        .background(
            RoundedRectangle(cornerRadius: 7, style: .continuous)
                .fill(Color.white.opacity(0.17))
        )
        .overlay(
            RoundedRectangle(cornerRadius: 7, style: .continuous)
                .stroke(Color.white.opacity(0.28), lineWidth: 1)
        )
        .frame(maxWidth: isCompactBar ? 30 : 170)
    }

    private func topBarMenuLabel(title: String, systemImage: String) -> some View {
        HStack(spacing: 4) {
            Image(systemName: systemImage)
                .font(.system(size: 11, weight: .semibold))

            if !isCompactBar {
                Text(title)
            }
        }
        .font(.system(size: 11, weight: .semibold, design: .monospaced))
        .foregroundStyle(Color.white.opacity(0.95))
        .padding(.horizontal, 8)
        .padding(.vertical, 5)
        .background(
            RoundedRectangle(cornerRadius: 7, style: .continuous)
                .fill(Color.white.opacity(0.17))
        )
        .overlay(
            RoundedRectangle(cornerRadius: 7, style: .continuous)
                .stroke(Color.white.opacity(0.28), lineWidth: 1)
        )
    }
}

private struct ITSoRCubeLogoView: View {
    var body: some View {
        GeometryReader { proxy in
            let logoSize = min(proxy.size.width, proxy.size.height)
            let scale = logoSize / 96
            let offsetX = (proxy.size.width - logoSize) / 2
            let offsetY = (proxy.size.height - logoSize) / 2
            let strokeWidth = max(1, 2 * scale)

            let point: (CGFloat, CGFloat) -> CGPoint = { x, y in
                CGPoint(x: offsetX + (x * scale), y: offsetY + (y * scale))
            }

            ZStack {
                Path { path in
                    path.move(to: point(48, 12))
                    path.addLine(to: point(76, 28))
                    path.addLine(to: point(48, 44))
                    path.addLine(to: point(20, 28))
                    path.closeSubpath()
                }
                .fill(LinearGradient(colors: [Color(hex: 0x4F46E5), Color(hex: 0x7C3AED)], startPoint: .topLeading, endPoint: .bottomTrailing))

                Path { path in
                    path.move(to: point(20, 28))
                    path.addLine(to: point(48, 44))
                    path.addLine(to: point(48, 78))
                    path.addLine(to: point(20, 62))
                    path.closeSubpath()
                }
                .fill(LinearGradient(colors: [Color(hex: 0x312E81), Color(hex: 0x5B21B6)], startPoint: .topLeading, endPoint: .bottomTrailing))

                Path { path in
                    path.move(to: point(76, 28))
                    path.addLine(to: point(48, 44))
                    path.addLine(to: point(48, 78))
                    path.addLine(to: point(76, 62))
                    path.closeSubpath()
                }
                .fill(LinearGradient(colors: [Color(hex: 0xA855F7), Color(hex: 0xEC4899)], startPoint: .topLeading, endPoint: .bottomTrailing))

                Path { path in
                    path.move(to: point(48, 44))
                    path.addLine(to: point(61.5, 36.2))
                    path.addLine(to: point(48, 28.5))
                    path.addLine(to: point(34.5, 36.2))
                    path.closeSubpath()
                }
                .fill(Color(hex: 0xF472B6).opacity(0.85))

                Path { path in
                    path.move(to: point(48, 44))
                    path.addLine(to: point(48, 61.2))
                    path.addLine(to: point(34.5, 53.4))
                    path.addLine(to: point(34.5, 36.2))
                    path.closeSubpath()
                }
                .fill(Color(hex: 0x4338CA).opacity(0.65))

                Path { path in
                    path.move(to: point(48, 44))
                    path.addLine(to: point(48, 61.2))
                    path.addLine(to: point(61.5, 53.4))
                    path.addLine(to: point(61.5, 36.2))
                    path.closeSubpath()
                }
                .fill(Color(hex: 0xDB2777).opacity(0.55))

                Path { path in
                    path.move(to: point(48, 12))
                    path.addLine(to: point(48, 44))
                }
                .stroke(Color(hex: 0xF9A8D4).opacity(0.9), style: StrokeStyle(lineWidth: strokeWidth, lineCap: .round))

                Path { path in
                    path.move(to: point(20, 28))
                    path.addLine(to: point(48, 44))
                    path.addLine(to: point(76, 28))
                }
                .stroke(Color(hex: 0xF9A8D4).opacity(0.55), style: StrokeStyle(lineWidth: strokeWidth, lineCap: .round, lineJoin: .round))
            }
        }
        .aspectRatio(1, contentMode: .fit)
    }
}

private struct DomainResourceBladeView: View {
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass

    @Binding var selectedDomain: AppDomain?
    @Binding var selectedResource: AppResource?
    let resources: [AppResource]

    @State private var isDomainExpanded = true
    @State private var isResourceExpanded = true

    private var isCompact: Bool {
        horizontalSizeClass == .compact
    }

    var body: some View {
        BladePane(title: "Navigation", subtitle: "Choose domain and resource") {
            ScrollView {
                VStack(alignment: .leading, spacing: 12) {
                    HStack(spacing: 8) {
                        sectionLabel("Domain")
                        Spacer(minLength: 8)

                        Button {
                            withAnimation(.easeInOut(duration: 0.2)) {
                                isDomainExpanded.toggle()
                            }
                        } label: {
                            Label(
                                isDomainExpanded ? "Collapse" : "Expand",
                                systemImage: isDomainExpanded ? "chevron.up" : "chevron.down"
                            )
                            .font(.system(size: 11, weight: .semibold, design: .monospaced))
                            .foregroundStyle(ITSoRBrand.deepBlue)
                            .labelStyle(.iconOnly)
                            .frame(width: 24, height: 24)
                        }
                        .buttonStyle(.plain)
                        .background(
                            RoundedRectangle(cornerRadius: 6, style: .continuous)
                                .fill(Color.white.opacity(0.85))
                        )
                        .overlay(
                            RoundedRectangle(cornerRadius: 6, style: .continuous)
                                .stroke(ITSoRBrand.paneBorder.opacity(0.9), lineWidth: 1)
                        )
                    }

                    if isDomainExpanded || !isCompact {
                        LazyVStack(spacing: 8) {
                            ForEach(AppDomain.allCases) { domain in
                                BladeSelectionRow(
                                    title: domain.title,
                                    subtitle: domain.subtitle,
                                    icon: domain.iconName,
                                    isSelected: selectedDomain == domain
                                ) {
                                    selectedDomain = domain
                                    if isCompact {
                                        withAnimation(.easeInOut(duration: 0.2)) {
                                            isDomainExpanded = false
                                        }
                                    }
                                }
                            }
                        }
                    } else if let selectedDomain {
                        BladeSelectionRow(
                            title: selectedDomain.title,
                            subtitle: selectedDomain.subtitle,
                            icon: selectedDomain.iconName,
                            isSelected: true
                        ) {
                            withAnimation(.easeInOut(duration: 0.2)) {
                                isDomainExpanded = true
                            }
                        }
                    } else {
                        Text("Select a domain to continue.")
                            .font(.system(size: 12, weight: .regular, design: .monospaced))
                            .foregroundStyle(ITSoRBrand.textSecondary)
                            .padding(.horizontal, 4)
                            .padding(.vertical, 8)
                    }

                    Rectangle()
                        .fill(ITSoRBrand.paneBorder.opacity(0.8))
                        .frame(height: 1)
                        .padding(.vertical, 2)

                    HStack(spacing: 8) {
                        sectionLabel("Resource")
                        Spacer(minLength: 8)

                        if !resources.isEmpty {
                            Button {
                                withAnimation(.easeInOut(duration: 0.2)) {
                                    isResourceExpanded.toggle()
                                }
                            } label: {
                                Label(
                                    isResourceExpanded ? "Collapse" : "Expand",
                                    systemImage: isResourceExpanded ? "chevron.up" : "chevron.down"
                                )
                                .font(.system(size: 11, weight: .semibold, design: .monospaced))
                                .foregroundStyle(ITSoRBrand.deepBlue)
                                .labelStyle(.iconOnly)
                                .frame(width: 24, height: 24)
                            }
                            .buttonStyle(.plain)
                            .background(
                                RoundedRectangle(cornerRadius: 6, style: .continuous)
                                    .fill(Color.white.opacity(0.85))
                            )
                            .overlay(
                                RoundedRectangle(cornerRadius: 6, style: .continuous)
                                    .stroke(ITSoRBrand.paneBorder.opacity(0.9), lineWidth: 1)
                            )
                        }
                    }

                    if resources.isEmpty {
                        Text("Choose a domain to load resources.")
                            .font(.system(size: 12, weight: .regular, design: .monospaced))
                            .foregroundStyle(ITSoRBrand.textSecondary)
                            .padding(.horizontal, 4)
                            .padding(.vertical, 8)
                    } else if isResourceExpanded || !isCompact {
                        LazyVStack(spacing: 8) {
                            ForEach(resources) { resource in
                                BladeSelectionRow(
                                    title: resource.title,
                                    subtitle: resource.subtitle,
                                    icon: resource.iconName,
                                    isSelected: selectedResource == resource
                                ) {
                                    selectedResource = resource
                                    if isCompact {
                                        withAnimation(.easeInOut(duration: 0.2)) {
                                            isResourceExpanded = false
                                        }
                                    }
                                }
                            }
                        }
                    } else if let selectedResource, resources.contains(selectedResource) {
                        BladeSelectionRow(
                            title: selectedResource.title,
                            subtitle: selectedResource.subtitle,
                            icon: selectedResource.iconName,
                            isSelected: true
                        ) {
                            withAnimation(.easeInOut(duration: 0.2)) {
                                isResourceExpanded = true
                            }
                        }
                    } else {
                        Text("Select a resource to continue.")
                            .font(.system(size: 12, weight: .regular, design: .monospaced))
                            .foregroundStyle(ITSoRBrand.textSecondary)
                            .padding(.horizontal, 4)
                            .padding(.vertical, 8)
                    }
                }
                .padding(12)
            }
        }
        .onChange(of: selectedDomain) { _, newValue in
            guard isCompact else { return }
            if newValue == nil {
                isDomainExpanded = true
                isResourceExpanded = true
                return
            }
            withAnimation(.easeInOut(duration: 0.2)) {
                isDomainExpanded = false
                isResourceExpanded = true
            }
        }
        .onChange(of: horizontalSizeClass) { _, newValue in
            if newValue != .compact {
                isDomainExpanded = true
                isResourceExpanded = true
            }
        }
    }

    private func sectionLabel(_ title: String) -> some View {
        Text(title)
            .font(.system(size: 11, weight: .bold, design: .monospaced))
            .foregroundStyle(ITSoRBrand.textSecondary)
            .textCase(.uppercase)
            .padding(.horizontal, 4)
    }
}

private enum WorkspaceCompactPane: String, CaseIterable, Identifiable {
    case list = "List"
    case detail = "Detail"

    var id: String { rawValue }
}

private struct AdaptiveWorkspaceView: View {
    let title: String
    let items: [BladeListItem]
    @Binding var selectedItemID: String?
    let isLoading: Bool
    let selectedResource: AppResource?
    let selectedTenant: Tenant?
    @Binding var editName: String
    let onList: () -> Void
    let onCreate: () -> Void
    let onConnect: () -> Void
    let onRead: () -> Void
    let onUpdate: () -> Void
    let onReplace: () -> Void
    let onDelete: () -> Void

    @State private var compactPane: WorkspaceCompactPane = .list

    var body: some View {
        GeometryReader { proxy in
            let useCompactLayout = proxy.size.width < 950

            Group {
                if useCompactLayout {
                    VStack(spacing: 0) {
                        Picker("Workspace Pane", selection: $compactPane) {
                            ForEach(WorkspaceCompactPane.allCases) { pane in
                                Text(pane.rawValue).tag(pane)
                            }
                        }
                        .pickerStyle(.segmented)
                        .padding(.horizontal, 10)
                        .padding(.vertical, 8)
                        .background(ITSoRBrand.surfaceTint.opacity(0.45))

                        if compactPane == .list {
                            listPane
                        } else {
                            detailPane
                        }
                    }
                } else {
                    HStack(spacing: 0) {
                        listPane
                            .frame(minWidth: 300, idealWidth: 360, maxWidth: 420)

                        Divider()

                        detailPane
                    }
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
        .onChange(of: selectedItemID) { _, newValue in
            if newValue != nil {
                compactPane = .detail
            }
        }
        .onChange(of: selectedResource) { _, _ in
            compactPane = .list
        }
    }

    private var listPane: some View {
        ListBladeView(
            title: title,
            items: items,
            selectedItemID: $selectedItemID,
            isLoading: isLoading,
            isResourceSelected: selectedResource != nil,
            canCreate: selectedResource == .tenants,
            canConnect: selectedResource == .tenants,
            onList: onList,
            onCreate: onCreate,
            onConnect: onConnect
        )
    }

    private var detailPane: some View {
        DetailBladeView(
            selectedResource: selectedResource,
            selectedTenant: selectedTenant,
            editName: $editName,
            isLoading: isLoading,
            onRead: onRead,
            onUpdate: onUpdate,
            onReplace: onReplace,
            onDelete: onDelete
        )
    }
}

private struct ListBladeView: View {
    let title: String
    let items: [BladeListItem]
    @Binding var selectedItemID: String?
    let isLoading: Bool
    let isResourceSelected: Bool
    let canCreate: Bool
    let canConnect: Bool
    let onList: () -> Void
    let onCreate: () -> Void
    let onConnect: () -> Void

    private var hasSecondaryActions: Bool {
        canCreate || canConnect
    }

    var body: some View {
        BladePane(
            title: "List",
            subtitle: isResourceSelected ? "\(title) collection" : "Select a resource to continue",
            actions: {
                ViewThatFits(in: .horizontal) {
                    HStack(spacing: 8) {
                        listButton
                        createButton
                        connectButton
                    }

                    HStack(spacing: 8) {
                        listButton
                        if hasSecondaryActions {
                            Menu {
                                createButton
                                connectButton
                            } label: {
                                Label("More", systemImage: "ellipsis.circle")
                            }
                            .buttonStyle(BrandSecondaryButtonStyle())
                        }
                    }
                }
            }
        ) {
            if !isResourceSelected {
                BladeEmptyStateView(
                    icon: "square.grid.2x2",
                    title: "Select a Resource",
                    message: "Choose a resource from the Resource blade."
                )
            } else if isLoading && items.isEmpty {
                VStack(spacing: 10) {
                    ProgressView()
                    Text("Loading \(title)…")
                        .font(.system(size: 12, weight: .regular, design: .monospaced))
                        .foregroundStyle(ITSoRBrand.textSecondary)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else if items.isEmpty {
                BladeEmptyStateView(
                    icon: "tray",
                    title: "No \(title)",
                    message: "Use List to load records from the API."
                )
            } else {
                ScrollView {
                    LazyVStack(spacing: 8) {
                        ForEach(items) { item in
                            BladeSelectionRow(
                                title: item.title,
                                subtitle: item.subtitle,
                                icon: "doc.text",
                                isSelected: selectedItemID == item.id
                            ) {
                                selectedItemID = item.id
                            }
                        }
                    }
                    .padding(12)
                }
            }
        }
    }

    private var listButton: some View {
        Button("List") {
            onList()
        }
        .disabled(!isResourceSelected || isLoading)
        .buttonStyle(BrandPrimaryButtonStyle())
    }

    @ViewBuilder
    private var createButton: some View {
        if canCreate {
            Button("Create") {
                onCreate()
            }
            .disabled(isLoading)
            .buttonStyle(BrandSecondaryButtonStyle())
        }
    }

    @ViewBuilder
    private var connectButton: some View {
        if canConnect {
            Button("Connect") {
                onConnect()
            }
            .buttonStyle(BrandPrimaryButtonStyle())
        }
    }
}

private struct DetailBladeView: View {
    let selectedResource: AppResource?
    let selectedTenant: Tenant?
    @Binding var editName: String
    let isLoading: Bool
    let onRead: () -> Void
    let onUpdate: () -> Void
    let onReplace: () -> Void
    let onDelete: () -> Void

    private var subtitle: String {
        if let selectedResource {
            if selectedResource == .tenants, let selectedTenant {
                return selectedTenant.name
            }
            return "\(selectedResource.title) detail"
        }
        return "Choose an item to inspect"
    }

    var body: some View {
        BladePane(title: "Detail", subtitle: subtitle) {
            Group {
                if selectedResource == nil {
                    BladeEmptyStateView(
                        icon: "sidebar.leading",
                        title: "Select a Resource",
                        message: "Pick a resource from the left to view details."
                    )
                } else if selectedResource != .tenants {
                    BladeEmptyStateView(
                        icon: "wrench.and.screwdriver",
                        title: "Resource Not Wired",
                        message: "Full detail actions are currently available for Tenants."
                    )
                } else if let tenant = selectedTenant {
                    TenantDetailFormView(
                        tenant: tenant,
                        name: $editName,
                        isLoading: isLoading,
                        onRead: onRead,
                        onUpdate: onUpdate,
                        onReplace: onReplace,
                        onDelete: onDelete
                    )
                } else {
                    BladeEmptyStateView(
                        icon: "doc.text.magnifyingglass",
                        title: "Select an Item",
                        message: "Choose a record from the List blade."
                    )
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
    }
}

private struct TenantDetailFormView: View {
        let tenant: Tenant
        @Binding var name: String
        let isLoading: Bool
        let onRead: () -> Void
        let onUpdate: () -> Void
        let onReplace: () -> Void
        let onDelete: () -> Void

        var body: some View {
            ScrollView {
                VStack(alignment: .leading, spacing: 12) {
                    BladeSectionCard(title: "Tenant") {
                        BladeInfoRow(label: "ID", value: tenant.id)
                        BladeInfoRow(label: "Owner", value: tenant.ownerId ?? "-")
                        BladeInfoRow(label: "Group", value: tenant.groupId ?? "-")
                        BladeInfoRow(label: "Permissions", value: "\(tenant.permissions)")
                    }

                    BladeSectionCard(title: "Editable") {
                        Text("Name")
                            .font(.system(size: 12, weight: .semibold, design: .monospaced))
                            .foregroundStyle(ITSoRBrand.textSecondary)

                        TextField("Tenant name", text: $name)
                            .textFieldStyle(.plain)
                            .font(.system(size: 13, weight: .regular, design: .monospaced))
                            .padding(.horizontal, 10)
                            .padding(.vertical, 8)
                            .background(
                                RoundedRectangle(cornerRadius: 8, style: .continuous)
                                    .fill(Color.white)
                            )
                            .overlay(
                                RoundedRectangle(cornerRadius: 8, style: .continuous)
                                    .stroke(ITSoRBrand.paneBorder, lineWidth: 1)
                            )
                    }

                    BladeSectionCard(title: "Operations") {
                        HStack(spacing: 8) {
                            Button("Read") { onRead() }
                                .disabled(isLoading)
                                .frame(maxWidth: .infinity)
                                .buttonStyle(BrandSecondaryButtonStyle())

                            Button("Update") { onUpdate() }
                                .disabled(isLoading)
                                .frame(maxWidth: .infinity)
                                .buttonStyle(BrandPrimaryButtonStyle())
                        }

                        HStack(spacing: 8) {
                            Button("Replace") { onReplace() }
                                .disabled(isLoading)
                                .frame(maxWidth: .infinity)
                                .buttonStyle(BrandPrimaryButtonStyle())

                            Button("Delete") { onDelete() }
                                .disabled(isLoading)
                                .frame(maxWidth: .infinity)
                                .buttonStyle(BrandDestructiveButtonStyle())
                        }
                    }
                }
                .padding(12)
            }
            .background(ITSoRBrand.paneContentBackground)
        }
    }

    private struct BladePane<Content: View, Actions: View>: View {
        @Environment(\.horizontalSizeClass) private var horizontalSizeClass

        let title: String
        let subtitle: String
        @ViewBuilder let actions: () -> Actions
        @ViewBuilder let content: () -> Content

        private var isCompact: Bool {
            horizontalSizeClass == .compact
        }

        init(title: String, subtitle: String, @ViewBuilder content: @escaping () -> Content) where Actions == EmptyView {
            self.title = title
            self.subtitle = subtitle
            self.actions = { EmptyView() }
            self.content = content
        }

        init(
            title: String,
            subtitle: String,
            @ViewBuilder actions: @escaping () -> Actions,
            @ViewBuilder content: @escaping () -> Content
        ) {
            self.title = title
            self.subtitle = subtitle
            self.actions = actions
            self.content = content
        }

        var body: some View {
            VStack(spacing: 0) {
                HStack(alignment: .top, spacing: 8) {
                    VStack(alignment: .leading, spacing: 3) {
                        Text(title)
                            .font(.system(size: isCompact ? 13 : 14, weight: .bold, design: .monospaced))
                            .foregroundStyle(ITSoRBrand.textPrimary)

                        Text(subtitle)
                            .font(.system(size: isCompact ? 11 : 12, weight: .regular, design: .monospaced))
                            .foregroundStyle(ITSoRBrand.textSecondary)
                            .lineLimit(2)
                    }

                    Spacer(minLength: 8)

                    HStack(spacing: isCompact ? 6 : 8) {
                        actions()
                    }
                }
                .padding(.horizontal, isCompact ? 10 : 12)
                .padding(.vertical, isCompact ? 8 : 10)
                .background(ITSoRBrand.paneHeaderBackground)

                Rectangle()
                    .fill(ITSoRBrand.paneBorder)
                    .frame(height: 1)

                content()
                    .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .topLeading)
                    .background(ITSoRBrand.paneContentBackground)
            }
            .background(ITSoRBrand.paneSurface)
            .clipShape(RoundedRectangle(cornerRadius: isCompact ? 10 : 14, style: .continuous))
            .overlay(
                RoundedRectangle(cornerRadius: isCompact ? 10 : 14, style: .continuous)
                    .stroke(ITSoRBrand.paneBorder, lineWidth: 1)
            )
            .shadow(color: ITSoRBrand.deepBlue.opacity(0.08), radius: isCompact ? 8 : 14, y: 4)
            .padding(isCompact ? 4 : 8)
        }
    }

    private struct BladeSelectionRow: View {
        @Environment(\.horizontalSizeClass) private var horizontalSizeClass

        let title: String
        let subtitle: String
        let icon: String
        let isSelected: Bool
        let action: () -> Void

        private var isCompact: Bool {
            horizontalSizeClass == .compact
        }

        var body: some View {
            Button(action: action) {
                HStack(alignment: .top, spacing: 10) {
                    Image(systemName: icon)
                        .font(.system(size: isCompact ? 12 : 14, weight: .semibold))
                        .foregroundStyle(isSelected ? Color.white.opacity(0.95) : ITSoRBrand.deepBlue.opacity(0.85))
                        .frame(width: isCompact ? 16 : 18, height: isCompact ? 16 : 18)
                        .padding(.top, 2)

                    VStack(alignment: .leading, spacing: 3) {
                        Text(title)
                            .font(.system(size: isCompact ? 12 : 13, weight: .bold, design: .monospaced))
                            .foregroundStyle(isSelected ? .white : ITSoRBrand.textPrimary)
                            .frame(maxWidth: .infinity, alignment: .leading)

                        Text(subtitle)
                            .font(.system(size: isCompact ? 11 : 12, weight: .regular, design: .monospaced))
                            .foregroundStyle(isSelected ? Color.white.opacity(0.86) : ITSoRBrand.textSecondary)
                            .lineLimit(isCompact ? 1 : 2)
                            .frame(maxWidth: .infinity, alignment: .leading)
                    }
                }
                .padding(.horizontal, isCompact ? 8 : 10)
                .padding(.vertical, isCompact ? 7 : 9)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(
                    RoundedRectangle(cornerRadius: 10, style: .continuous)
                        .fill(
                            isSelected
                            ? LinearGradient(
                                colors: [ITSoRBrand.deepBlue, ITSoRBrand.purple, ITSoRBrand.hotPink],
                                startPoint: .leading,
                                endPoint: .trailing
                            )
                            : LinearGradient(
                                colors: [Color.white.opacity(0.96), ITSoRBrand.surfaceTint.opacity(0.8)],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                        )
                )
                .overlay(
                    RoundedRectangle(cornerRadius: 10, style: .continuous)
                        .stroke(
                            isSelected ? Color.white.opacity(0.2) : ITSoRBrand.paneBorder.opacity(0.8),
                            lineWidth: 1
                        )
                )
                .shadow(color: ITSoRBrand.deepBlue.opacity(isSelected ? 0.22 : 0.06), radius: isSelected ? (isCompact ? 7 : 10) : 4, y: 2)
            }
            .buttonStyle(.plain)
        }
    }

    private struct BladeEmptyStateView: View {
        @Environment(\.horizontalSizeClass) private var horizontalSizeClass

        let icon: String
        let title: String
        let message: String

        private var isCompact: Bool {
            horizontalSizeClass == .compact
        }

        var body: some View {
            VStack(spacing: 10) {
                Image(systemName: icon)
                    .font(.system(size: isCompact ? 22 : 28, weight: .semibold))
                    .foregroundStyle(ITSoRBrand.purple.opacity(0.75))

                Text(title)
                    .font(.system(size: isCompact ? 18 : 22, weight: .bold, design: .monospaced))
                    .foregroundStyle(ITSoRBrand.textPrimary)

                Text(message)
                    .font(.system(size: isCompact ? 12 : 13, weight: .regular, design: .monospaced))
                    .foregroundStyle(ITSoRBrand.textSecondary)
                    .multilineTextAlignment(.center)
                    .frame(maxWidth: 320)
            }
            .padding(isCompact ? 16 : 24)
            .frame(maxWidth: .infinity, maxHeight: .infinity)
        }
    }

    private struct BladeSectionCard<Content: View>: View {
        let title: String
        @ViewBuilder let content: () -> Content

        var body: some View {
            VStack(alignment: .leading, spacing: 10) {
                Text(title)
                    .font(.system(size: 12, weight: .bold, design: .monospaced))
                    .foregroundStyle(ITSoRBrand.textSecondary)
                    .textCase(.uppercase)

                content()
            }
            .padding(12)
            .background(
                RoundedRectangle(cornerRadius: 10, style: .continuous)
                    .fill(Color.white.opacity(0.96))
            )
            .overlay(
                RoundedRectangle(cornerRadius: 10, style: .continuous)
                    .stroke(ITSoRBrand.paneBorder, lineWidth: 1)
            )
        }
    }

    private struct BladeInfoRow: View {
        let label: String
        let value: String

        var body: some View {
            HStack(alignment: .firstTextBaseline, spacing: 10) {
                Text(label)
                    .font(.system(size: 12, weight: .semibold, design: .monospaced))
                    .foregroundStyle(ITSoRBrand.textSecondary)

                Spacer(minLength: 8)

                Text(value)
                    .font(.system(size: 12, weight: .regular, design: .monospaced))
                    .foregroundStyle(ITSoRBrand.textPrimary)
                    .multilineTextAlignment(.trailing)
            }
        }
    }

private struct CreateTenantView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var name = ""

    let onCreate: (TenantDraft) -> Void

    var body: some View {
        NavigationStack {
            Form {
                TextField("Name", text: $name)
            }
            .navigationTitle("Create Tenant")
            .tint(ITSoRBrand.purple)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Create") {
                        onCreate(TenantDraft(name: name))
                        dismiss()
                    }
                    .disabled(name.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                }
            }
        }
    }
}

private struct ConnectionView: View {
    @Environment(\.dismiss) private var dismiss
    @Binding var serverURL: String
    @Binding var identifier: String
    @Binding var signupUsername: String
    @Binding var signupEmail: String
    @Binding var password: String
    let onLogin: () -> Void
    let onSignup: () -> Void

    var body: some View {
        NavigationStack {
            Form {
                Section("Server") {
                    TextField("Base URL", text: $serverURL)
                    Text("iOS simulator: use http://127.0.0.1:8000")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                    Text("Physical iPhone: use your Mac LAN IP, e.g. http://192.168.1.20:8000")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }

                Section("Credentials") {
                    TextField("Email or Username", text: $identifier)
                    SecureField("Password", text: $password)
                }

                Section("Signup") {
                    TextField("Username", text: $signupUsername)
                    TextField("Email", text: $signupEmail)
#if os(iOS)
                        .textInputAutocapitalization(.never)
#endif
                    Text("Signup uses the same password field above.")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
            }
            .navigationTitle("Connect")
            .tint(ITSoRBrand.purple)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Close") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    HStack {
                        Button("Signup") {
                            onSignup()
                            dismiss()
                        }
                        .disabled(signupUsername.isEmpty || signupEmail.isEmpty || password.isEmpty)

                        Button("Login") {
                            onLogin()
                            dismiss()
                        }
                        .disabled(identifier.isEmpty || password.isEmpty)
                    }
                }
            }
        }
    }
}

@MainActor
private final class BladeViewModel: ObservableObject {
    @Published var selectedDomain: AppDomain?
    @Published var selectedResource: AppResource?
    @Published var selectedItemID: String?

    @Published var tenants: [Tenant] = []
    @Published var editName = ""

    @Published var serverURLText = "http://127.0.0.1:8000"
    @Published var identifier = ""
    @Published var signupUsername = ""
    @Published var signupEmail = ""
    @Published var password = ""
    @Published var searchText = ""
    @Published var statusMessage: String?
    @Published var isLoading = false

    private let api = TenantAPIClient()
    private var accessToken: String?

    var resourcesForSelectedDomain: [AppResource] {
        selectedDomain?.resources ?? []
    }

    var listBladeTitle: String {
        selectedResource?.title ?? "Items"
    }

    var listItems: [BladeListItem] {
        let unfilteredItems: [BladeListItem]
        switch selectedResource {
        case .tenants:
            unfilteredItems = tenants.map {
                BladeListItem(id: $0.id, title: $0.name, subtitle: "ID: \($0.id)")
            }
        case .none, .users, .groups, .permissions, .roles:
            unfilteredItems = []
        }

        let normalizedQuery = searchText.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !normalizedQuery.isEmpty else {
            return unfilteredItems
        }

        return unfilteredItems.filter { item in
            item.title.localizedCaseInsensitiveContains(normalizedQuery)
            || item.subtitle.localizedCaseInsensitiveContains(normalizedQuery)
        }
    }

    var selectedTenant: Tenant? {
        guard selectedResource == .tenants, let selectedItemID else { return nil }
        return tenants.first(where: { $0.id == selectedItemID })
    }

    var tenantMenuOptions: [Tenant] {
        tenants.sorted { left, right in
            left.name.localizedCaseInsensitiveCompare(right.name) == .orderedAscending
        }
    }

    var activeTenantName: String {
        selectedTenant?.name ?? "All Tenants"
    }

    var globalSearchResults: [TopBarSearchResult] {
        let normalizedQuery = searchText.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !normalizedQuery.isEmpty else {
            return []
        }

        var results: [TopBarSearchResult] = []

        for resource in AppResource.allCases where
            resource.title.localizedCaseInsensitiveContains(normalizedQuery)
            || resource.subtitle.localizedCaseInsensitiveContains(normalizedQuery) {
            results.append(
                TopBarSearchResult(
                    target: .resource(resource),
                    title: resource.title,
                    subtitle: resource.subtitle,
                    iconName: resource.iconName
                )
            )
        }

        for tenant in tenantMenuOptions where
            tenant.name.localizedCaseInsensitiveContains(normalizedQuery)
            || tenant.id.localizedCaseInsensitiveContains(normalizedQuery) {
            results.append(
                TopBarSearchResult(
                    target: .tenant(tenant.id),
                    title: tenant.name,
                    subtitle: "Tenant • \(tenant.id)",
                    iconName: "building.2"
                )
            )
        }

        return Array(results.prefix(10))
    }

    func ensureDefaultSelection() async {
        if selectedDomain == nil {
            selectedDomain = AppDomain.platform
        }
        if selectedResource == nil {
            selectedResource = resourcesForSelectedDomain.first
        }
    }

    func handleDomainChanged() {
        let resources = resourcesForSelectedDomain
        if !resources.contains(where: { $0 == selectedResource }) {
            selectedResource = resources.first
        }
        selectedItemID = nil
        syncEditorWithSelection()
    }

    func handleResourceChanged(from previous: AppResource?, to current: AppResource?) {
        guard previous != current else { return }

        if current == .tenants,
           let selectedItemID,
           tenants.contains(where: { $0.id == selectedItemID }) {
            syncEditorWithSelection()
            return
        }

        selectedItemID = nil
        syncEditorWithSelection()
    }

    func selectTenantFromMenu(id: String?) {
        selectedDomain = .platform
        selectedResource = .tenants

        if let id {
            selectedItemID = id
            if let selected = tenants.first(where: { $0.id == id }) {
                editName = selected.name
            }
            statusMessage = "Tenant context set to \(tenants.first(where: { $0.id == id })?.name ?? id)"
        } else {
            selectedItemID = nil
            editName = ""
            statusMessage = "Tenant context set to All Tenants"
        }
    }

    func submitGlobalSearch() {
        guard let firstResult = globalSearchResults.first else {
            statusMessage = "No matches for \"\(searchText)\""
            return
        }
        activateGlobalSearchResult(firstResult)
    }

    func activateGlobalSearchResult(_ result: TopBarSearchResult) {
        switch result.target {
        case .resource(let resource):
            selectedDomain = .platform
            selectedResource = resource
            statusMessage = "Opened \(resource.title)"
        case .tenant(let tenantID):
            selectTenantFromMenu(id: tenantID)
        }
    }

    func signOut() {
        accessToken = nil
        password = ""
        searchText = ""
        statusMessage = "Signed out"
    }

    func login() async {
        await perform("Logged in") {
            api.setBaseURL(serverURLText)
            let response = try await api.login(identifier: identifier, password: password)
            accessToken = response.accessToken
        }
    }

    func signup() async {
        await perform("Signed up and logged in") {
            api.setBaseURL(serverURLText)
            let response = try await api.signup(username: signupUsername, email: signupEmail, password: password)
            accessToken = response.accessToken
            identifier = signupEmail
        }
    }

    func listSelectedResource() async {
        switch selectedResource {
        case .tenants:
            await listTenants()
        case .users, .groups, .permissions, .roles:
            statusMessage = "List not yet wired for \(selectedResource?.title ?? "resource")"
        case .none:
            statusMessage = "Select a resource first"
        }
    }

    func listTenants() async {
        await perform("Listed tenants") {
            guard let token = accessToken else {
                statusMessage = "Connect first (tap Connect → Login)"
                return
            }
            tenants = try await api.listTenants(token: token)
            if selectedTenant == nil {
                selectedItemID = tenants.first?.id
            }
            syncEditorWithSelection()
        }
    }

    func createTenant(from draft: TenantDraft) async {
        await perform("Created tenant") {
            guard let token = accessToken else {
                statusMessage = "Connect first (tap Connect → Login)"
                return
            }
            let created = try await api.createTenant(draft, token: token)
            tenants.insert(created, at: 0)
            selectedItemID = created.id
            selectedResource = .tenants
            syncEditorWithSelection()
        }
    }

    func readSelectedTenant() async {
        guard let selectedItemID else {
            statusMessage = "Select a tenant first"
            return
        }

        await perform("Read tenant") {
            guard let token = accessToken else {
                statusMessage = "Connect first (tap Connect → Login)"
                return
            }
            let fresh = try await api.readTenant(id: selectedItemID, token: token)
            merge(tenant: fresh)
            syncEditorWithSelection()
        }
    }

    func updateSelectedTenant() async {
        guard let selectedItemID else {
            statusMessage = "Select a tenant first"
            return
        }

        await perform("Updated tenant") {
            guard let token = accessToken else {
                statusMessage = "Connect first (tap Connect → Login)"
                return
            }
            let patch = TenantPatch(name: emptyToNil(editName))
            let updated = try await api.updateTenant(id: selectedItemID, patch: patch, token: token)
            merge(tenant: updated)
            syncEditorWithSelection()
        }
    }

    func replaceSelectedTenant() async {
        guard let selectedItemID else {
            statusMessage = "Select a tenant first"
            return
        }

        await perform("Replaced tenant") {
            guard let token = accessToken else {
                statusMessage = "Connect first (tap Connect → Login)"
                return
            }
            let replacement = TenantDraft(name: editName)
            let replaced = try await api.replaceTenant(id: selectedItemID, with: replacement, token: token)
            merge(tenant: replaced)
            syncEditorWithSelection()
        }
    }

    func deleteSelectedTenant() async {
        guard let selectedItemID else {
            statusMessage = "Select a tenant first"
            return
        }

        await perform("Deleted tenant") {
            guard let token = accessToken else {
                statusMessage = "Connect first (tap Connect → Login)"
                return
            }
            try await api.deleteTenant(id: selectedItemID, token: token)
            tenants.removeAll(where: { $0.id == selectedItemID })
            self.selectedItemID = tenants.first?.id
            syncEditorWithSelection()
        }
    }

    private func perform(_ successMessage: String, action: () async throws -> Void) async {
        isLoading = true
        defer { isLoading = false }

        do {
            try await action()
            statusMessage = successMessage
        } catch {
            statusMessage = "API error: \(error.localizedDescription)"
        }
    }

    private func merge(tenant: Tenant) {
        if let index = tenants.firstIndex(where: { $0.id == tenant.id }) {
            tenants[index] = tenant
        } else {
            tenants.insert(tenant, at: 0)
        }
    }

    private func syncEditorWithSelection() {
        guard let selected = selectedTenant else {
            editName = ""
            return
        }
        editName = selected.name
    }

    private func emptyToNil(_ value: String) -> String? {
        let trimmed = value.trimmingCharacters(in: .whitespacesAndNewlines)
        return trimmed.isEmpty ? nil : trimmed
    }
}

private enum ITSoRBrand {
    static let deepBlue = Color(hex: 0x1F2A7A)
    static let purple = Color(hex: 0x6D28D9)
    static let hotPink = Color(hex: 0xEC4899)
    static let surfaceTint = Color(hex: 0xF7F4FF)
    static let appBackgroundTop = Color(hex: 0xF6F5FB)
    static let appBackgroundBottom = Color(hex: 0xEFEFF6)
    static let textPrimary = Color(hex: 0x1F2937)
    static let textSecondary = Color(hex: 0x4B5563)
    static let paneSurface = Color.white.opacity(0.97)
    static let paneHeaderBackground = Color.white.opacity(0.95)
    static let paneContentBackground = Color(hex: 0xF8F7FD)
    static let paneBorder = Color(hex: 0xC9D1E6).opacity(0.88)
}

private struct BrandPrimaryButtonStyle: ButtonStyle {
    @Environment(\.isEnabled) private var isEnabled
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass

    private var isCompact: Bool {
        horizontalSizeClass == .compact
    }

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: isCompact ? 12 : 13, weight: .semibold, design: .monospaced))
            .foregroundStyle(.white.opacity(isEnabled ? 1 : 0.75))
            .padding(.horizontal, isCompact ? 10 : 12)
            .padding(.vertical, isCompact ? 5 : 6)
            .background(
                RoundedRectangle(cornerRadius: 8, style: .continuous)
                    .fill(
                        LinearGradient(
                            colors: [ITSoRBrand.deepBlue, ITSoRBrand.purple, ITSoRBrand.hotPink],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 8, style: .continuous)
                    .stroke(Color.white.opacity(0.2), lineWidth: 1)
            )
            .opacity(isEnabled ? (configuration.isPressed ? 0.82 : 1) : 0.45)
    }
}

private struct BrandSecondaryButtonStyle: ButtonStyle {
    @Environment(\.isEnabled) private var isEnabled
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass

    private var isCompact: Bool {
        horizontalSizeClass == .compact
    }

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: isCompact ? 12 : 13, weight: .semibold, design: .monospaced))
            .foregroundStyle(ITSoRBrand.deepBlue.opacity(isEnabled ? 1 : 0.75))
            .padding(.horizontal, isCompact ? 10 : 12)
            .padding(.vertical, isCompact ? 5 : 6)
            .background(
                RoundedRectangle(cornerRadius: 8, style: .continuous)
                    .fill(
                        Color.white.opacity(isEnabled ? (configuration.isPressed ? 0.9 : 0.98) : 0.85)
                    )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 8, style: .continuous)
                    .stroke(ITSoRBrand.purple.opacity(0.34), lineWidth: 1)
            )
            .opacity(isEnabled ? 1 : 0.6)
    }
}

private struct BrandDestructiveButtonStyle: ButtonStyle {
    @Environment(\.isEnabled) private var isEnabled
    @Environment(\.horizontalSizeClass) private var horizontalSizeClass

    private var isCompact: Bool {
        horizontalSizeClass == .compact
    }

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: isCompact ? 12 : 13, weight: .semibold, design: .monospaced))
            .foregroundStyle(.white.opacity(isEnabled ? 1 : 0.75))
            .padding(.horizontal, isCompact ? 10 : 12)
            .padding(.vertical, isCompact ? 5 : 6)
            .background(
                RoundedRectangle(cornerRadius: 8, style: .continuous)
                    .fill(
                        LinearGradient(
                            colors: [Color(hex: 0xBE185D), ITSoRBrand.hotPink],
                            startPoint: .leading,
                            endPoint: .trailing
                        )
                    )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 8, style: .continuous)
                    .stroke(Color.white.opacity(0.2), lineWidth: 1)
            )
            .opacity(isEnabled ? (configuration.isPressed ? 0.85 : 1) : 0.45)
    }
}

private extension Color {
    init(hex: UInt32) {
        self.init(
            .sRGB,
            red: Double((hex >> 16) & 0xFF) / 255,
            green: Double((hex >> 8) & 0xFF) / 255,
            blue: Double(hex & 0xFF) / 255,
            opacity: 1
        )
    }
}

private enum AppDomain: String, CaseIterable, Identifiable {
    case platform

    var id: String { rawValue }

    var iconName: String {
        switch self {
        case .platform:
            return "square.stack.3d.up.fill"
        }
    }

    var title: String {
        switch self {
        case .platform:
            return "Platform"
        }
    }

    var subtitle: String {
        switch self {
        case .platform:
            return "Core service APIs"
        }
    }

    var resources: [AppResource] {
        switch self {
        case .platform:
            return [.tenants, .users, .groups, .roles, .permissions]
        }
    }
}

private enum AppResource: String, CaseIterable, Identifiable {
    case tenants
    case users
    case groups
    case roles
    case permissions

    var id: String { rawValue }

    var iconName: String {
        switch self {
        case .tenants:
            return "building.2.fill"
        case .users:
            return "person.2.fill"
        case .groups:
            return "person.3.fill"
        case .roles:
            return "person.badge.key.fill"
        case .permissions:
            return "checkmark.shield.fill"
        }
    }

    var title: String {
        switch self {
        case .tenants:
            return "Tenants"
        case .users:
            return "Users"
        case .groups:
            return "Groups"
        case .roles:
            return "Roles"
        case .permissions:
            return "Permissions"
        }
    }

    var subtitle: String {
        switch self {
        case .tenants:
            return "Tenant CRUD"
        case .users:
            return "User identities"
        case .groups:
            return "Group memberships"
        case .roles:
            return "Role assignments"
        case .permissions:
            return "Permission registry"
        }
    }
}

private struct BladeListItem: Identifiable, Hashable {
    let id: String
    let title: String
    let subtitle: String
}

private enum TopBarSearchTarget: Hashable {
    case resource(AppResource)
    case tenant(String)
}

private struct TopBarSearchResult: Identifiable, Hashable {
    let target: TopBarSearchTarget
    let title: String
    let subtitle: String
    let iconName: String

    var id: String {
        switch target {
        case .resource(let resource):
            return "resource:\(resource.rawValue)"
        case .tenant(let tenantID):
            return "tenant:\(tenantID)"
        }
    }
}

private struct Tenant: Codable, Identifiable, Hashable {
    let id: String
    let name: String
    let ownerId: String?
    let groupId: String?
    let permissions: Int

    enum CodingKeys: String, CodingKey {
        case id
        case name
        case ownerId = "owner_id"
        case groupId = "group_id"
        case permissions
    }
}

private struct TenantDraft: Codable {
    let name: String
}

private struct TenantPatch: Codable {
    let name: String?
}

private struct LoginRequest: Codable {
    let identifier: String
    let password: String
}

private struct SignupRequest: Codable {
    let username: String
    let email: String
    let password: String
}

private struct TokenResponse: Codable {
    let accessToken: String

    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
    }
}

private final class TenantAPIClient {
    private var baseURL = URL(string: "http://127.0.0.1:8000")!
    private let decoder = JSONDecoder()
    private let encoder = JSONEncoder()

    func setBaseURL(_ value: String) {
        let trimmed = value.trimmingCharacters(in: .whitespacesAndNewlines)
        if let parsed = URL(string: trimmed), parsed.scheme != nil, parsed.host != nil {
            baseURL = parsed
        }
    }

    func login(identifier: String, password: String) async throws -> TokenResponse {
        try await request(path: "/login", method: "POST", token: nil, body: LoginRequest(identifier: identifier, password: password))
    }

    func signup(username: String, email: String, password: String) async throws -> TokenResponse {
        try await request(path: "/signup", method: "POST", token: nil, body: SignupRequest(username: username, email: email, password: password))
    }

    func listTenants(token: String) async throws -> [Tenant] {
        try await request(path: "/tenants", method: "GET", token: token)
    }

    func createTenant(_ draft: TenantDraft, token: String) async throws -> Tenant {
        try await request(path: "/tenants", method: "POST", token: token, body: draft)
    }

    func readTenant(id: String, token: String) async throws -> Tenant {
        try await request(path: "/tenants/\(id)", method: "GET", token: token)
    }

    func updateTenant(id: String, patch: TenantPatch, token: String) async throws -> Tenant {
        try await request(path: "/tenants/\(id)", method: "PATCH", token: token, body: patch)
    }

    func replaceTenant(id: String, with replacement: TenantDraft, token: String) async throws -> Tenant {
        try await request(path: "/tenants/\(id)", method: "PUT", token: token, body: replacement)
    }

    func deleteTenant(id: String, token: String) async throws {
        let _: EmptyAPIResponse = try await request(path: "/tenants/\(id)", method: "DELETE", token: token)
    }

    private func request<Response: Decodable>(path: String, method: String, token: String?) async throws -> Response {
        let url = baseURL.appending(path: path)
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        if let token {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        return try await execute(request)
    }

    private func request<Response: Decodable, RequestBody: Encodable>(path: String, method: String, token: String?, body: RequestBody) async throws -> Response {
        let url = baseURL.appending(path: path)
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        if let token {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }
        request.httpBody = try encoder.encode(body)

        return try await execute(request)
    }

    private func execute<Response: Decodable>(_ request: URLRequest) async throws -> Response {
        let data: Data
        let response: URLResponse
        do {
            (data, response) = try await URLSession.shared.data(for: request)
        } catch let urlError as URLError {
            throw APIError.transport(urlError)
        } catch {
            throw APIError.unknown(error)
        }

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }

        guard (200...299).contains(httpResponse.statusCode) else {
            throw APIError.httpStatus(code: httpResponse.statusCode)
        }

        if Response.self == EmptyAPIResponse.self {
            return EmptyAPIResponse() as! Response
        }

        do {
            return try decoder.decode(Response.self, from: data)
        } catch {
            throw APIError.decodingFailed
        }
    }
}

private struct EmptyAPIResponse: Decodable {}

private enum APIError: LocalizedError {
    case invalidResponse
    case httpStatus(code: Int)
    case decodingFailed
    case transport(URLError)
    case unknown(Error)

    var errorDescription: String? {
        switch self {
        case .invalidResponse:
            return "Invalid response from server"
        case .httpStatus(let code):
            return "Server returned status \(code)"
        case .decodingFailed:
            return "Failed to decode server response"
        case .transport(let error):
            if error.code == .cannotFindHost {
                return "Hostname not found. In iOS Simulator use http://127.0.0.1:8000. On a physical iPhone use your Mac LAN IP (for example http://192.168.1.20:8000)."
            }
            return error.localizedDescription
        case .unknown(let error):
            return error.localizedDescription
        }
    }
}

#Preview {
    ContentView()
}
