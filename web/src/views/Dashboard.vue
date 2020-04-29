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
      v-for="(deviceLine, index) in deviceListShow"
      :key="index"
    >
      <vs-col
        type="flex"
        vs-justify="center"
        vs-align="center"
        vs-w="2"
        vs-xs="12"
        class="cardx"
        v-for="(device, index) in deviceLine"
        :key="index"
      >
        <vs-card class="bg-dark">
          <div slot="header">
            <h3>高清片源</h3>
          </div>
          <div slot="media">
            <video
              :id="device.id"
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
                      params: { camera_id: device.id }
                    })
                    .catch(() => {})
                "
                >配置</vs-button
              >
              <vs-button
                color="danger"
                type="gradient"
                @click="fullScreen(device.id)"
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
          const elem = document.getElementById(device.id);
          this.hls.push(hls);
          hls.loadSource("http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8");
          hls.attachMedia(elem);
          hls.on(Hls.Events.MANIFEST_PARSED, function() {
            elem.play();
          });
        }
      }
    },

    getDevice() {
      const path = "http://192.168.43.69:7101/get_device";
      axios
        .get(path)
        .then(res => {
          this.deviceListShow = res.data.deviceListShow;
          this.deviceList = res.data.deviceList;
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
