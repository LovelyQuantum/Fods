<!-- =========================================================================================
    File Name: Error404.vue
    Description: 404 Page
    ----------------------------------------------------------------------------------------
    Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
      Author: Pixinvent
    Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== -->

<template>
  <div>
    <div class="vx-row">
      <div class="vx-col w-full sm:w-1/2 md:w-1/2 lg:w-1/4 xl:w-1/4">
        <statistics-card-line
          hideChart
          class="mb-base"
          icon="CpuIcon"
          icon-right
          :statistic="systemUpDay"
          statisticTitle="系统运行时间"
        />
      </div>

      <div class="vx-col w-full sm:w-1/2 md:w-1/2 lg:w-1/4 xl:w-1/4">
        <statistics-card-line
          hideChart
          class="mb-base"
          icon="ServerIcon"
          icon-right
          statistic="正常"
          statisticTitle="系统工作状态"
          color="success"
        />
      </div>

      <div class="vx-col w-full sm:w-1/2 md:w-1/2 lg:w-1/4 xl:w-1/4">
        <statistics-card-line
          hideChart
          class="mb-base"
          icon="ActivityIcon"
          icon-right
          :statistic="warmingTimes"
          statisticTitle="预警次数"
          color="warning"
        />
      </div>

      <div class="vx-col w-full sm:w-1/2 md:w-1/2 lg:w-1/4 xl:w-1/4">
        <statistics-card-line
          hideChart
          class="mb-base"
          icon="AlertOctagonIcon"
          icon-right
          :statistic="exWarmingTimes"
          statisticTitle="严重预警次数"
          color="danger"
        />
      </div>
    </div>
    <div class="vx-col w-full">
      <div class="vx-row w-1/4 flex"></div>
      <vx-card title="预警统计" class="mb-base mt-5">
        <template slot="actions"></template>
        <div slot="no-body" class="p-6 pb-0">
          <div class="vx-row mb-1">
            <div class="my-auto ml-5 mr-5"><span>范围查询</span></div>
            <datepicker
              :language="zh"
              :format="dateFormatter"
              placeholder="起始日期"
              v-model="dateRangeBegin"
              class="my-auto"
            ></datepicker>
            <div class="my-auto ml-5 mr-5"><span>—</span></div>
            <datepicker
              :language="zh"
              :format="dateFormatter"
              placeholder="截至日期"
              v-model="dateRangeEnd"
              class="my-auto"
            ></datepicker>
            <vs-button
              color="primary"
              type="filled"
              class="ml-5"
              @click="recordRangeCheck"
              >查询</vs-button
            >
            <vs-button
              color="primary"
              type="filled"
              class="ml-5"
              @click="clearDateRange()"
              >重置</vs-button
            >
          </div>
          <div class="vx-row mb-1">
            <p class="ml-10" v-if="recordQueryMessage">
              {{ recordQueryMessage }}
            </p>
          </div>
          <vue-apex-charts
            type="line"
            height="266"
            :options="chartOptions"
            :series="recordSeries"
          />
        </div>
      </vx-card>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import VueApexCharts from "vue-apexcharts";
import Datepicker from "vuejs-datepicker";
import moment from "moment";
import { zh } from "vuejs-datepicker/dist/locale";
import StatisticsCardLine from "@/components/statistics-cards/StatisticsCardLine.vue";

export default {
  components: {
    VueApexCharts,
    StatisticsCardLine,
    Datepicker
  },
  data() {
    return {
      zh: zh,
      dateFormat: "yyyy-MM-dd",
      dateRangeBegin: null,
      dateRangeEnd: null,
      recordQueryMessage: null,
      systemUpDay: "0 天",
      warmingTimes: "0 次",
      exWarmingTimes: "0 次",
      recordSeries: {},
      chartOptions: {
        chart: {
          toolbar: { show: false },
          zoom: { enabled: false },
          dropShadow: {
            enabled: true,
            top: 5,
            left: 0,
            blur: 4,
            opacity: 0.1
          }
        },
        stroke: {
          curve: "smooth",
          dashArray: [0, 0],
          width: [4, 4]
        },
        grid: {
          borderColor: "#e7e7e7"
        },
        legend: {
          show: false
        },
        colors: ["#18a1a5", "#F97794"],
        fill: {
          type: "gradient",
          gradient: {
            shade: "dark",
            inverseColors: false,
            gradientToColors: ["#27c573", "#7367F0"],
            shadeIntensity: 1,
            type: "horizontal",
            opacityFrom: 1,
            opacityTo: 1,
            stops: [0, 100, 100, 100]
          }
        },
        markers: {
          size: 0,
          hover: {
            size: 5
          }
        },
        xaxis: {
          labels: {
            style: {
              cssClass: "text-grey fill-current"
            }
          },
          axisTicks: {
            show: false
          },
          // categories: ["01", "05", "09", "13", "17", "21", "26", "31"],
          axisBorder: {
            show: false
          }
        },
        yaxis: {
          tickAmount: 5,
          labels: {
            style: {
              cssClass: "text-grey fill-current"
            },
            formatter(val) {
              return val > 999 ? `${(val / 1000).toFixed(1)}k` : val;
            }
          }
        },
        tooltip: {
          x: { show: false }
        }
      }
    };
  },
  methods: {
    dateFormatter(date) {
      return moment(date).format("YYYY-MM-DD");
    },

    clearDateRange() {
      this.dateRangeBegin = null;
      this.dateRangeEnd = null;
      this.recordQueryMessage = null;
      this.recordSeriesQuery();
    },
    systemInfoQuery() {
      const path = "http://192.168.20.25:8081/apis/system_info";
      axios.get(path).then(res => {
        this.systemUpDay = res.data.systemUpDay + " 天";
        this.warmingTimes = res.data.warmingTimes + "次";
        this.exWarmingTimes = res.data.exWarmingTimes + "次";
      });
    },

    recordSeriesQuery() {
      const path = "http://192.168.20.25:8081/apis/fod_record_report";
      const data = {
        dateRange: {
          dateRangeBegin: this.dateRangeBegin,
          dateRangeEnd: this.dateRangeEnd
        }
      };
      axios.post(path, data).then(res => {
        this.recordSeries = res.data.recordSeries;
      });
    },

    recordRangeCheck() {
      if (this.dateRangeBegin && this.dateRangeEnd) {
        const beginDate =
          this.dateRangeBegin.getFullYear() +
          " 年 " +
          (this.dateRangeBegin.getMonth() + 1) +
          " 月 " +
          this.dateRangeBegin.getDate() +
          " 日";
        const endDate =
          this.dateRangeEnd.getFullYear() +
          " 年 " +
          (this.dateRangeEnd.getMonth() + 1) +
          " 月 " +
          this.dateRangeEnd.getDate() +
          " 日";
        this.recordQueryMessage =
          "已查询到 " + beginDate + "  至  " + endDate + " 之间的记录";
        this.recordSeriesQuery();
      }
    }
  },
  created() {
    this.systemInfoQuery();
    this.recordSeriesQuery();
  }
};
</script>
