//
//  ContentView.swift
//  ITSoR
//
//  Created by Nathan McGuire on 2/27/26.
//

import SwiftUI
import Combine

struct ContentView: View {
    @StateObject private var viewModel = TenantsViewModel()
    @State private var showingCreateForm = false
    @State private var showingConnectionSheet = false

    var body: some View {
        NavigationSplitView {
            List(viewModel.tenants, selection: $viewModel.selectedTenantID) { tenant in
                VStack(alignment: .leading, spacing: 4) {
                    Text(tenant.name)
                        .font(.headline)
                        .lineLimit(1)
                    Text("ID: \(tenant.id)")
                        .font(.caption)
                        .foregroundStyle(.secondary)
                }
                .tag(tenant.id)
            }
            .overlay {
                if viewModel.tenants.isEmpty && !viewModel.isLoading {
                    ContentUnavailableView("No Tenants", systemImage: "tray", description: Text("Tap List after connecting to the API."))
                }
            }
            .navigationTitle("API CRUD Demo")
            .toolbar {
                ToolbarItemGroup {
                    Button("Connect") {
                        showingConnectionSheet = true
                    }

                    Button("List") {
                        Task { await viewModel.listTenants() }
                    }

                    Button("Create") {
                        showingCreateForm = true
                    }
                }
            }
            .sheet(isPresented: $showingCreateForm) {
                CreateTenantView { draft in
                    Task { await viewModel.createTenant(from: draft) }
                }
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
            }
        } detail: {
            if let tenant = viewModel.selectedTenant {
                TenantDetailView(
                    name: $viewModel.editName,
                    tenant: tenant,
                    isLoading: viewModel.isLoading,
                    onRead: { Task { await viewModel.readSelectedTenant() } },
                    onUpdate: { Task { await viewModel.updateSelectedTenant() } },
                    onReplace: { Task { await viewModel.replaceSelectedTenant() } },
                    onDelete: { Task { await viewModel.deleteSelectedTenant() } }
                )
            } else {
                ContentUnavailableView("Select a Tenant", systemImage: "doc.text.magnifyingglass", description: Text("Connect, run List, then select a tenant."))
            }
        }
        .overlay(alignment: .bottom) {
            if let status = viewModel.statusMessage {
                Text(status)
                    .font(.footnote)
                    .padding(.horizontal, 14)
                    .padding(.vertical, 8)
                    .background(.ultraThinMaterial, in: Capsule())
                    .padding(.bottom, 10)
            }
        }
        .task {
            if viewModel.tenants.isEmpty {
                await viewModel.listTenants()
            }
        }
    }
}

private struct TenantDetailView: View {
    @Binding var name: String
    let tenant: Tenant
    let isLoading: Bool
    let onRead: () -> Void
    let onUpdate: () -> Void
    let onReplace: () -> Void
    let onDelete: () -> Void

    var body: some View {
        Form {
            Section("Selected") {
                LabeledContent("ID", value: tenant.id)
                LabeledContent("Owner", value: tenant.ownerId ?? "-")
            }

            Section("Editable") {
                TextField("Name", text: $name)
            }

            Section("Operations") {
                Button("Read") { onRead() }
                    .disabled(isLoading)
                Button("Update (PATCH)") { onUpdate() }
                    .disabled(isLoading)
                Button("Replace (PUT)") { onReplace() }
                    .disabled(isLoading)
                Button("Delete") { onDelete() }
                    .disabled(isLoading)
                    .foregroundStyle(.red)
            }
        }
        .navigationTitle(tenant.name)
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
private final class TenantsViewModel: ObservableObject {
    @Published var tenants: [Tenant] = []
    @Published var selectedTenantID: String?
    @Published var editName = ""
    @Published var serverURLText = "http://127.0.0.1:8000"
    @Published var identifier = ""
    @Published var signupUsername = ""
    @Published var signupEmail = ""
    @Published var password = ""
    @Published var statusMessage: String?
    @Published var isLoading = false

    private let api = TenantAPIClient()
    private var accessToken: String?

    var selectedTenant: Tenant? {
        guard let selectedTenantID else { return nil }
        return tenants.first(where: { $0.id == selectedTenantID })
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

    func listTenants() async {
        await perform("Listed tenants") {
            guard let token = accessToken else {
                statusMessage = "Connect first (tap Connect → Login)"
                return
            }
            tenants = try await api.listTenants(token: token)
            if selectedTenant == nil {
                selectedTenantID = tenants.first?.id
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
            selectedTenantID = created.id
            syncEditorWithSelection()
        }
    }

    func readSelectedTenant() async {
        guard let selectedTenantID else {
            statusMessage = "Select a tenant first"
            return
        }

        await perform("Read tenant") {
            guard let token = accessToken else {
                statusMessage = "Connect first (tap Connect → Login)"
                return
            }
            let fresh = try await api.readTenant(id: selectedTenantID, token: token)
            merge(tenant: fresh)
            syncEditorWithSelection()
        }
    }

    func updateSelectedTenant() async {
        guard let selectedTenantID else {
            statusMessage = "Select a tenant first"
            return
        }

        await perform("Updated tenant") {
            guard let token = accessToken else {
                statusMessage = "Connect first (tap Connect → Login)"
                return
            }
            let patch = TenantPatch(name: emptyToNil(editName))
            let updated = try await api.updateTenant(id: selectedTenantID, patch: patch, token: token)
            merge(tenant: updated)
            syncEditorWithSelection()
        }
    }

    func replaceSelectedTenant() async {
        guard let selectedTenantID else {
            statusMessage = "Select a tenant first"
            return
        }

        await perform("Replaced tenant") {
            guard let token = accessToken else {
                statusMessage = "Connect first (tap Connect → Login)"
                return
            }
            let replacement = TenantDraft(name: editName)
            let replaced = try await api.replaceTenant(id: selectedTenantID, with: replacement, token: token)
            merge(tenant: replaced)
            syncEditorWithSelection()
        }
    }

    func deleteSelectedTenant() async {
        guard let selectedTenantID else {
            statusMessage = "Select a tenant first"
            return
        }

        await perform("Deleted tenant") {
            guard let token = accessToken else {
                statusMessage = "Connect first (tap Connect → Login)"
                return
            }
            try await api.deleteTenant(id: selectedTenantID, token: token)
            tenants.removeAll(where: { $0.id == selectedTenantID })
            self.selectedTenantID = tenants.first?.id
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
        guard let selected = selectedTenant else { return }
        editName = selected.name
    }

    private func emptyToNil(_ value: String) -> String? {
        let trimmed = value.trimmingCharacters(in: .whitespacesAndNewlines)
        return trimmed.isEmpty ? nil : trimmed
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
