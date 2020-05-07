/* eslint-disable vue/valid-v-for */ /* eslint-disable vue/valid-v-for */
<!-- =========================================================================================
  File Name: DashboardAnalytics.vue
  Description: Dashboard Analytics
  ----------------------------------------------------------------------------------------
  Item Name: Vuexy - Vuejs, HTML & Laravel Admin Dashboard Template
  Author: Pixinvent
  Author URL: http://www.themeforest.net/user/pixinvent
========================================================================================== -->

<template>
  <div id="dashboard-analytics">
    <vs-row
      vs-justify="center"
      v-for="(num, idx) of parseInt(deviceNum / 5 + 1)"
      :key="idx"
    >
      <vs-col
        type="flex"
        vs-justify="center"
        vs-align="center"
        vs-w="2"
        vs-xs="12"
        class="cardx"
        v-for="(device, index) of deviceList.slice(idx * 5, (idx + 1) * 5)"
        :key="index"
      >
        <vs-card class="bg-dark">
          <div slot="header">
            <h3>{{device.deviceName}}</h3>
          </div>
          <div slot="media">
            <video
              :id="device.name"
              height="100%"
              width="100%"
              muted
              draggable="false"
            ></video>
          </div>
          <div slot="footer">
            <vs-row vs-justify="flex-end">
              <vs-button
                color="primary"
                type="gradient"
                @click="
                  $router
                    .push({
                      name: 'device-camera',
                      params: { camera_id: device.name }
                    })
                    .catch(() => {})
                "
                >配置</vs-button
              >
              <vs-button
                color="danger"
                type="gradient"
                @click="fullScreen(device.name)"
                >全屏</vs-button
              >
            </vs-row>
          </div>
        </vs-card>
      </vs-col>
    </vs-row>
  </div>
</template>

<script>
import Hls from "hls.js";
import axios from "axios";
export default {
  name: "dHelp",
  data() {
    return {
      deviceListShow: [],
      deviceList: [],
      deviceNum: 0,
      hls: ""
    };
  },
  methods: {
    destroyHls() {
      if (this.hls) {
        for (let h of this.hls) {
          h.destroy();
          this.hls = [];
        }
      }
    },
    loadVideoFn() {
      if (Hls.isSupported()) {
        this.hls = [];
        for (let device of this.deviceList) {
          const hls = new Hls();
          const elem = document.getElementById(device.name);
          this.hls.push(hls);
          hls.loadSource(device.sourcePath);
          hls.attachMedia(elem);
          hls.on(Hls.Events.MANIFEST_PARSED, function() {
            elem.play();
          });
        }
      }
    },

    getDevice() {
      const path = "http://192.168.43.69:8081/apis/get_device_info";
      axios
        .get(path)
        .then(res => {
          this.deviceList = res.data.deviceList;
          this.deviceNum = res.data.deviceNum;
        })
        .then(() => {
          this.loadVideoFn();
        });
    },

    fullScreen: function(e) {
      let elem = document.getElementById(e);
      if (elem.requestFullscreen) {
        elem.requestFullscreen();
      } else if (elem.mozRequestFullScreen) {
        elem.mozRequestFullScreen();
      } else if (elem.webkitRequestFullscreen) {
        elem.webkitRequestFullscreen();
      } else if (elem.msRequestFullscreen) {
        elem.msRequestFullscreen();
      }
    }
  },

  mounted() {
    this.getDevice();
  },

  beforeDestroy() {
    this.destroyHls();
  }
};
</script>

<style>
.cardx {
  margin-right: 20px;
  margin-top: 20px;
}
@media (max-width: 800px) {
  .cardx {
    margin-right: 0px;
    margin-top: 0px;
  }
}
@media (min-width: 1300px) {
  .cardx {
    margin-top: 30px;
    margin-right: 40px;
  }
}
video::-webkit-media-controls {
  display: none !important;
}
</style>
