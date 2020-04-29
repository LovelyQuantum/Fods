<!-- =========================================================================================
    File Name: Error404.vue
    Description: 404 Page
    ----------------------------------------------------------------------------------------
    Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
      Author: Pixinvent
    Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== -->

<template>
  <div class="vx-row">
    <div class="vx-col w-full md:w-1/3 mb-base">
      <div>
        <statistics-card-line
          class="md:mb-0 mb-base"
          icon="UserCheckIcon"
          icon-right
          statistic="CPU利用率"
          :chartData="activeUsers.series"
        />
      </div>
      <div class="mt-5">
        <statistics-card-line
          class="md:mb-0 mb-base"
          icon="UserCheckIcon"
          icon-right
          statistic="GPU利用率"
          :chartData="activeUsers.series"
        />
      </div>
    </div>
    <div class="vx-col w-full md:w-1/3 mb-base">
      <vx-card title="系统占用率">
        <!-- CHART -->
        <template slot="no-body">
          <div class="mt-5 mb-10">
            <vue-apex-charts
              type="radialBar"
              height="300"
              :options="goalOverviewRadialBar.chartOptions"
              :series="goalOverviewRadialBar.series"
            />
          </div>
        </template>
        <!-- DATA -->
        <div
          class="flex justify-between text-center mt-6"
          slot="no-body-bottom"
        >
          <div
            class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0 border-l-0"
          >
            <p class="mt-4">剩余磁盘空间</p>
            <p class="mb-4 text-3xl font-semibold">786G</p>
          </div>
          <div
            class="w-1/2 border border-solid d-theme-border-grey-light border-r-0 border-b-0"
          >
            <p class="mt-4">进程数</p>
            <p class="mb-4 text-3xl font-semibold">13,561</p>
          </div>
        </div>
      </vx-card>
    </div>

    <div class="vx-col w-full md:w-1/3 lg:w-1/3 xl:w-1/3 mb-base">
      <vx-card title="系统摘要">
        <div
          v-for="(browser, index) in browserAnalytics"
          :key="browser.id"
          :class="{ 'mt-4': index }"
        >
          <div class="flex justify-between">
            <div class="flex flex-col">
              <span class="mb-1">{{ browser.name }}</span>
              <h4>{{ browser.ratio }}%</h4>
            </div>
            <div class="flex flex-col text-right">
              <span class="flex -mr-1">
                <span class="text-grey">{{ browser.time | time(true) }}</span>
              </span>
            </div>
          </div>
          <vs-progress :percent="browser.ratio"></vs-progress>
        </div>
      </vx-card>
    </div>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts";
import StatisticsCardLine from "@/components/statistics-cards/StatisticsCardLine.vue";

export default {
  components: {
    VueApexCharts,
    StatisticsCardLine
  },
  data() {
    return {
      goalOverviewRadialBar: {
        chartOptions: {
          plotOptions: {
            radialBar: {
              size: 110,
              startAngle: -150,
              endAngle: 150,
              hollow: {
                size: "77%"
              },
              track: {
                background: "#bfc5cc",
                strokeWidth: "50%"
              },
              dataLabels: {
                name: {
                  show: false
                },
                value: {
                  offsetY: 18,
                  color: "#99a2ac",
                  fontSize: "4rem"
                }
              }
            }
          },
          colors: ["#00db89"],
          fill: {
            type: "gradient",
            gradient: {
              shade: "dark",
              type: "horizontal",
              shadeIntensity: 0.5,
              gradientToColors: ["#00b5b5"],
              inverseColors: true,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 100]
            }
          },
          stroke: {
            lineCap: "round"
          },
          chart: {
            sparkline: {
              enabled: true
            },
            dropShadow: {
              enabled: true,
              blur: 3,
              left: 1,
              top: 1,
              opacity: 0.1
            }
          }
        },
        analyticsData: {
          completed: 786617,
          inProgress: 13561
        },
        series: [83]
      },
      activeUsers: {
        series: [
          {
            name: "Active Users",
            data: [750, 1000, 900, 1250, 1000, 1200, 1100]
          }
        ]
      },
      browserAnalytics: [
        {
          id: 1,
          name: "磁盘使用率",
          ratio: 73,
          time: "Mon Dec 10 2018 07:46:05 GMT+0000 (GMT)",
          comparedResult: "800"
        },
        {
          id: 3,
          name: "CPU使用率",
          ratio: 8,
          time: "Mon Dec 10 2018 07:46:05 GMT+0000 (GMT)",
          comparedResult: "-200"
        },
        {
          id: 2,
          name: "GPU使用率",
          ratio: 19,
          time: "Mon Dec 10 2018 07:46:05 GMT+0000 (GMT)",
          comparedResult: "100"
        },
        {
          id: 4,
          name: "内存使用率",
          ratio: 27,
          time: "Mon Dec 10 2018 07:46:05 GMT+0000 (GMT)",
          comparedResult: "-450"
        }
      ],
      supportTracker: {
        analyticsData: {
          openTickets: 163,
          meta: {
            "New Tickets": 29,
            "Open Tickets": 63,
            "Response Time": "1d"
          }
        },
        series: [83]
      }
    };
  }
};
</script>
