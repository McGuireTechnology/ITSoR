import { useQuery } from "@tanstack/react-query"
import { useRouterState } from "@tanstack/react-router"
import { Briefcase, Home, Users } from "lucide-react"

import { SidebarAppearance } from "@/components/Common/Appearance"
import { Logo } from "@/components/Common/Logo"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
} from "@/components/ui/sidebar"
import useAuth from "@/hooks/useAuth"
import {
  buildNavigationFromOpenApi,
  getNavigation,
  toTitle,
} from "@/lib/apiNavigation"
import { type Item, Main } from "./Main"
import { User } from "./User"

const getPathSegments = (pathname: string) =>
  pathname.split("/").filter(Boolean)
const reservedRoutes = new Set(["admin", "items", "settings"])

export function AppSidebar() {
  const { user: currentUser } = useAuth()
  const pathname = useRouterState({
    select: (state) => state.location.pathname,
  })
  const { data: navigation } = useQuery({
    queryFn: getNavigation,
    queryKey: ["api-navigation"],
    staleTime: 1000 * 60 * 10,
    retry: 1,
    placeholderData: buildNavigationFromOpenApi({}),
  })
  const [appFromPath = "default"] = getPathSegments(pathname)
  const selectedApp =
    !appFromPath || reservedRoutes.has(appFromPath) ? "default" : appFromPath

  const appSections = navigation?.[selectedApp]
  const appItems: Item[] = Object.entries(appSections ?? {}).flatMap(
    ([section, resources]) => {
      return [...resources]
        .sort((left, right) => left.localeCompare(right))
        .map((resource) => ({
          icon: resource === "users" ? Users : Briefcase,
          title: toTitle(resource),
          subtitle: toTitle(section),
          path: `/${selectedApp}/${section}/${resource}`,
        }))
    },
  )

  const items: Item[] = [
    { icon: Home, title: "Dashboard", path: `/${selectedApp}` },
    ...appItems.filter((item) => {
      if (item.title === "Users" && !currentUser?.is_superuser) {
        return false
      }
      return true
    }),
  ]

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="itsor-gradient-surface px-4 py-6 group-data-[collapsible=icon]:px-0 group-data-[collapsible=icon]:items-center">
        <Logo variant="responsive" />
      </SidebarHeader>
      <SidebarContent>
        <Main items={items} />
      </SidebarContent>
      <SidebarFooter>
        <SidebarAppearance />
        <User user={currentUser} />
      </SidebarFooter>
    </Sidebar>
  )
}

export default AppSidebar
