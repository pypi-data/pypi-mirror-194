import gqlDynamicRoutes from "../components/app/dynamicRoutes.graphql";

/**
 * Vue mixin containing code getting dynamically added routes from other apps.
 *
 * Only used by main App component, but factored out for readability.
 */
const routesMixin = {
  data() {
    return {
      dynamicRoutes: null,
    };
  },
  apollo: {
    dynamicRoutes: {
      query: gqlDynamicRoutes,
      pollInterval: 60000,
    },
  },
  watch: {
    dynamicRoutes: {
      handler(newDynamicRoutes) {
        for (const route of newDynamicRoutes) {
          if (route) {
            console.debug("Adding new dynamic route:", route.routeName);
            let routeEntry = {
              path: route.routePath,
              name: route.routeName,
              component: () => import("../components/LegacyBaseTemplate.vue"),
              props: {
                byTheGreatnessOfTheAlmightyAleksolotlISwearIAmWorthyOfUsingTheLegacyBaseTemplate: true,
              },
              meta: {
                inMenu: route.displaySidenavMenu,
                inAccountMenu: route.displayAccountMenu,
                icon: route.menuIcon,
                rawTitleString: route.menuTitle,
                menuPermission: route.menuPermission,
                permission: route.routePermission,
                newTab: route.menuNewTab,
              },
            };

            if (route.parentRouteName) {
              this.$router.addRoute(route.parentRouteName, routeEntry);
            } else {
              this.$router.addRoute(routeEntry);
            }
          }
        }

        this.getPermissionNames();
        this.buildMenus();
      },
      deep: true,
    },
  },
};

export default routesMixin;
