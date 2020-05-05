/*=========================================================================================
  File Name: sidebarItems.js
  Description: Sidebar Items list. Add / Remove menu items from here.
  Strucutre:
          url     => router path
          name    => name to display in sidebar
          slug    => router path name
          icon    => Feather Icon component/icon name
          tag     => text to display on badge
          tagColor  => class to apply on badge element
          i18n    => Internationalization
          submenu   => submenu of current item (current item will become dropdown )
                NOTE: Submenu don't have any icon(you can add icon if u want to display)
          isDisabled  => disable sidebar item/group
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
==========================================================================================*/

export default [
  {
    url: "/dashboard",
    slug: "dashboard",
    name: "预览",
    icon: "TvIcon"
  },
  {
    header: "设备",
    items: [
      {
        url: null,
        name: "摄像头",
        icon: "VideoIcon",
        submenu: [
          {
            url: "/device/camera/camera01",
            slug: "device-cmera-01",
            name: "摄像头1"
          },
          {
            url: "/device/camera/camera02",
            slug: "device-cmera-01",
            name: "摄像头2"
          },
          {
            url: "/device/camera/camera03",
            slug: "device-cmera-01",
            name: "摄像头3"
          },
          {
            url: "/device/camera/camera04",
            slug: "device-cmera-01",
            name: "摄像头4"
          },
          {
            url: "/device/camera/camera05",
            slug: "device-cmera-01",
            name: "摄像头5"
          },
          {
            url: "/device/camera/camera06",
            slug: "device-cmera-01",
            name: "摄像头6"
          },
          {
            url: "/device/camera/camera07",
            slug: "device-cmera-01",
            name: "摄像头7"
          },
          {
            url: "/device/camera/camera08",
            slug: "device-cmera-01",
            name: "摄像头8"
          },
          {
            url: "/device/camera/camera09",
            slug: "device-cmera-01",
            name: "摄像头9"
          },
          {
            url: "/device/camera/camera10",
            slug: "device-cmera-01",
            name: "摄像头10"
          }
        ]
      }
    ]
  },

  {
    header: "系统",
    items: [
      {
        url: "/system/report",
        name: "统计信息",
        icon: "PieChartIcon"
      },
      {
        url: "/system/record",
        slug: "system-record",
        name: "预警记录",
        icon: "CalendarIcon"
      },
      {
        url: "/system/settings",
        slug: "system-settings",
        name: "系统配置",
        icon: "SettingsIcon"
      },
      {
        url: "/system/info",
        slug: "system-info",
        name: "系统信息",
        icon: "InfoIcon"
      }
    ]
  }
];
