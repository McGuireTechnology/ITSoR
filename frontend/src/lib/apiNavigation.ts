import { OpenAPI } from "@/client"

export type ResourceLocation = {
  app: string
  section: string
  resource: string
}

export type AppNavigation = Record<string, Record<string, Set<string>>>

const API_VERSION_PREFIX = "/api/v1/"

const NON_RESOURCE_PATHS = new Set(["login", "private", "utils"])

const normalizeSegment = (segment: string) =>
  segment.replace(/[{}]/g, "").trim().toLowerCase()

export const resourceLocationFromPath = (
  path: string,
): ResourceLocation | undefined => {
  if (!path.startsWith(API_VERSION_PREFIX)) {
    return undefined
  }

  const segments = path
    .slice(API_VERSION_PREFIX.length)
    .split("/")
    .map(normalizeSegment)
    .filter(Boolean)

  if (segments.length === 0) {
    return undefined
  }

  const [first] = segments
  if (!first || NON_RESOURCE_PATHS.has(first)) {
    return undefined
  }

  if (segments.length >= 3) {
    return {
      app: first,
      section: segments[1] || "core",
      resource: segments[2] || "overview",
    }
  }

  if (segments.length === 2) {
    return {
      app: "default",
      section: first,
      resource: segments[1] || "overview",
    }
  }

  return { app: "default", section: "core", resource: first }
}

export const buildNavigationFromOpenApi = (
  openApiPaths: Record<string, unknown>,
): AppNavigation => {
  const navigation: AppNavigation = {}

  for (const path of Object.keys(openApiPaths)) {
    const location = resourceLocationFromPath(path)
    if (!location) {
      continue
    }

    navigation[location.app] ??= {}
    navigation[location.app][location.section] ??= new Set<string>()
    navigation[location.app][location.section]?.add(location.resource)
  }

  if (Object.keys(navigation).length === 0) {
    navigation.default = { core: new Set(["items"]) }
  }

  return navigation
}

export const getNavigation = async (): Promise<AppNavigation> => {
  const openApiUrl = `${OpenAPI.BASE}/api/v1/openapi.json`
  const response = await fetch(openApiUrl, {
    credentials: "include",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("access_token") ?? ""}`,
    },
  })

  if (!response.ok) {
    throw new Error("Unable to load OpenAPI specification for navigation.")
  }

  const data = (await response.json()) as { paths?: Record<string, unknown> }
  return buildNavigationFromOpenApi(data.paths ?? {})
}

export const toTitle = (value: string) =>
  value
    .split(/[-_]/g)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ")
