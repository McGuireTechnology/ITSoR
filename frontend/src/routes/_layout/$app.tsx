import { createFileRoute } from "@tanstack/react-router"

import useAuth from "@/hooks/useAuth"
import { toTitle } from "@/lib/apiNavigation"

export const Route = createFileRoute("/_layout/$app")({
  component: AppDashboard,
})

function AppDashboard() {
  const { user: currentUser } = useAuth()
  const { app } = Route.useParams()

  return (
    <div>
      <h1 className="text-2xl truncate max-w-sm">
        {toTitle(app)} app · Hi, {currentUser?.full_name || currentUser?.email}{" "}
        👋
      </h1>
      <p className="text-muted-foreground">
        Select a section and resource from the left navigation.
      </p>
    </div>
  )
}
