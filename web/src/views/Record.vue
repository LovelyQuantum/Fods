<template>
  <vx-card class="w-5/6 mx-auto">
    <vs-table @selected="handleSelected" v-model="selected" :data="records">
      <template slot="header">
        <div>
          <h2>预警记录</h2>
          <div class="vx-row mb-1 mt-5">
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
              placeholder="截止日期"
              v-model="dateRangeEnd"
              class="my-auto"
            ></datepicker>
            <vs-button
              color="primary"
              type="filled"
              class="ml-5"
              @click="recordQuery"
              >查询</vs-button
            >
            <div class="my-auto ml-5 mr-5"><span>按摄像头查询</span></div>
            <vs-select v-model="dataDevice" class="my-auto">
              <vs-select-item
                :key="device.id"
                :value="device"
                :text="device.deviceName"
                v-for="device in devices"
                class="w-full"
              />
            </vs-select>
            <vs-button
              color="primary"
              type="filled"
              class="ml-5"
              @click="recordDeviceQuery"
              >查询</vs-button
            >
            <vs-button
              color="primary"
              type="filled"
              class="ml-5"
              @click="clearDateRange"
              >重置</vs-button
            >
          </div>
          <div class="vx-row mb-5">
            <p class="ml-10" v-if="recordQueryMessage">
              {{ recordQueryMessage }}
            </p>
          </div>
        </div>
      </template>
      <template slot="thead">
        <vs-th>序号</vs-th>
        <vs-th>时间</vs-th>
        <vs-th>设备名</vs-th>
        <vs-th>所属矿井</vs-th>
        <vs-th>级别</vs-th>
      </template>

      <template slot-scope="{ data }">
        <vs-tr :data="tr" :key="indextr" v-for="(tr, indextr) in data">
          <vs-td :data="data[indextr].id">
            {{ data[indextr].id }}
          </vs-td>
          <vs-td :data="data[indextr].timestamp">
            {{ data[indextr].timestamp }}
          </vs-td>
          <vs-td :data="data[indextr].deviceName">
            {{ data[indextr].deviceName }}
          </vs-td>
          <vs-td :data="data[indextr].deviceName">
            {{ data[indextr].location }}
          </vs-td>
          <vs-td :data="data[indextr].status">
            {{ data[indextr].status }}
          </vs-td>
        </vs-tr>
      </template>
    </vs-table>
    <vs-pagination
      :total="totalPages"
      v-model="currentx"
      class="mt-10"
    ></vs-pagination>
    <vs-popup
      class="holamundo"
      title="图像预览"
      :active.sync="previewPopupActive"
    >
      <img :src="previewSrc" class="w-full mx-auto" />
    </vs-popup>
  </vx-card>
</template>

<script>
import Datepicker from "vuejs-datepicker";
import moment from "moment";
import { zh } from "vuejs-datepicker/dist/locale";
import axios from "axios";

export default {
  components: {
    Datepicker
  },
  data() {
    return {
      zh: zh,
      selected: null,
      activeLine: null,
      dateRangeBegin: null,
      dateRangeEnd: null,
      dataDevice: null,
      recordQueryMessage: null,
      log: [],
      currentx: 1,
      previewPopupActive: false,
      totalPages: 1,
      previewSrc: null,
      records: [],
      devices: []
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
      this.dataDevice = null;
      this.recordQuery();
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
      }
    },

    loadDeviceInfo() {
      const path =
        "http://" + process.env.VUE_APP_SERVER_URL + "/apis/system_info";
      axios.get(path).then(res => {
        this.devices = res.data.devices;
      });
    },

    recordDeviceQuery() {
      this.recordRangeCheck();
      const path =
        "http://" + process.env.VUE_APP_SERVER_URL + "/apis/fod_device_record";
      const data = {
        dataDeviceId: this.dataDevice.id,
        dateRange: {
          dateRangeBegin: this.dateRangeBegin,
          dateRangeEnd: this.dateRangeEnd
        },
        Page: this.currentx
      };
      axios.post(path, data).then(res => {
        this.records = res.data.records;
        this.totalPages = res.data.totalPages;
      });
    },

    recordQuery() {
      this.recordRangeCheck();
      const path =
        "http://" + process.env.VUE_APP_SERVER_URL + "/apis/fod_record";
      const data = {
        dateRange: {
          dateRangeBegin: this.dateRangeBegin,
          dateRangeEnd: this.dateRangeEnd
        },
        Page: this.currentx
      };
      axios.post(path, data).then(res => {
        this.records = res.data.records;
        this.totalPages = res.data.totalPages;
      });
    },

    handleSelected(tr) {
      if (this.activeLine === tr) {
        this.selected = null;
        this.activeLine = null;
      } else {
        this.activeLine = tr;
        this.previewPopupActive = true;
        const path =
          "http://" +
          process.env.VUE_APP_SERVER_URL +
          "/apis/fod_record_preview";
        const data = { recordId: tr.id };
        axios.post(path, data).then(res => {
          this.previewSrc = res.data.previewSrc;
        });
      }
    }
  },
  created() {
    this.loadDeviceInfo();
    this.recordQuery();
  },
  watch: {
    currentx: function() {
      if (this.dataDevice) this.recordDeviceQuery();
      else this.recordQuery();
    }
  }
};
</script>
