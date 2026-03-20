import { useQuery } from "@tanstack/react-query"
import { useNavigate, useRouterState } from "@tanstack/react-router"

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { buildNavigationFromOpenApi, getNavigation } from "@/lib/apiNavigation"

const getCurrentApp = (pathname: string) => {
  const [app] = pathname.split("/").filter(Boolean)
  return app || "default"
}

const AppSwitcher = () => {
  const navigate = useNavigate()
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

  const currentApp = getCurrentApp(pathname)
  const appNames = Object.keys(navigation ?? {}).sort()

  if (appNames.length <= 1) {
    return null
  }

  return (
    <Select
      value={currentApp}
      onValueChange={(nextApp) => {
        navigate({
          to: "/$app",
          params: { app: nextApp },
        })
      }}
    >
      <SelectTrigger className="w-[180px]">
        <SelectValue placeholder="Select app" />
      </SelectTrigger>
      <SelectContent>
        {appNames.map((app) => (
          <SelectItem key={app} value={app}>
            {app}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  )
}

export default AppSwitcher
