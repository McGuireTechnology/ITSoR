import { createFileRoute } from "@tanstack/react-router"

import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { toTitle } from "@/lib/apiNavigation"
import { AdminPage } from "./admin"
import { ItemsPage } from "./items"

export const Route = createFileRoute("/_layout/$app/$section/$resource")({
  component: ResourceRoute,
})

function ResourceRoute() {
  const { app, section, resource } = Route.useParams()

  if (resource === "items") {
    return <ItemsPage />
  }

  if (resource === "users") {
    return <AdminPage />
  }

  return (
    <Alert>
      <AlertTitle>
        {toTitle(app)} / {toTitle(section)} / {toTitle(resource)}
      </AlertTitle>
      <AlertDescription>
        This resource was discovered from the backend OpenAPI schema, but a UI
        module has not been assigned yet.
      </AlertDescription>
    </Alert>
  )
}
