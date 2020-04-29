<template>
  <div class="flex">
    <div class="w-1/2">
      <vs-input v-model="device.id" style="display:none;" />

      <!-- camera config -->
      <vx-card title="配置" class="mb-base mt-10">
        <div class="vx-row flex">
          <vs-divider> 基础设置 </vs-divider>
          <div class="vx-col w-full md:w-1/2">
            <vs-input
              v-validate="'required|alpha_dash'"
              label-placeholder="设备名称"
              name="设备名称"
              v-model="device.name"
              class="w-full"
            />
            <span class="text-danger text-sm" v-show="errors.has('设备名称')">{{
              errors.first("设备名称")
            }}</span>
          </div>

          <div class="vx-col w-full md:w-1/2">
            <vs-input
              v-validate="'required|ip'"
              label-placeholder="设备ip"
              name="设备ip"
              v-model="device.ip"
              class="w-full"
            />
            <span class="text-danger text-sm" v-show="errors.has('设备ip')">{{
              errors.first("设备ip")
            }}</span>
          </div>
        </div>
        <div class="vx-row flex mb-10">
          <div class="vx-col w-full md:w-1/2">
            <vs-input
              v-validate="'required'"
              label-placeholder="用户名"
              name="用户名"
              v-model="device.username"
              class="w-full mt-10"
            />
            <span class="text-danger text-sm" v-show="errors.has('用户名')">{{
              errors.first("用户名")
            }}</span>
          </div>

          <div class="vx-col w-full md:w-1/2">
            <vs-input
              v-validate="'required'"
              label-placeholder="设备密码"
              name="设备密码"
              v-model="device.passwd"
              class="w-full mt-10"
            />
            <span class="text-danger text-sm" v-show="errors.has('设备密码')">{{
              errors.first("设备密码")
            }}</span>
          </div>
        </div>

        <!-- function selection -->
        <vs-divider> 功能 </vs-divider>
        <ul class="vx-row flex">
          <div class="vx-col  ml-5 w-full md:w-1/4">
            <li class="vx-auto">
              <label for="">皮带异物检测</label>
              <vs-switch
                v-model="switchs"
                vs-icon-off="close"
                vs-icon-on="done"
                vs-value="fod"
              />
            </li>
          </div>
          <div class="vx-col  ml-5 w-full md:w-1/4">
            <li class="vx-auto">
              <label for="">皮带跑偏检测</label>
              <vs-switch
                v-model="switchs"
                vs-icon-off="close"
                vs-icon-on="done"
                vs-value="bdd"
              />
            </li>
          </div>
        </ul>

        <template v-if="showTabs">
          <vs-divider> 高级 </vs-divider>
          <vs-tabs>
            <template v-if="switchs.includes('fod')">
              <vs-tab label="皮带异物检测">
                <p class="text-center">预警阈值</p>
                <div class="vx-row flex mb-5">
                  <div class="vx-col w-full md:w-1/6">
                    <vs-input
                      v-model="nWarningThreshold"
                      class="w-full"
                      disabled
                    />
                  </div>
                  <div class="vx-col w-full md:w-4/5">
                    <vs-slider
                      v-model="nWarningThreshold"
                      :min="200"
                      :max="1000"
                    />
                  </div>
                </div>
                <p class="text-center">严重预警阈值</p>
                <div class="vx-row flex">
                  <div class="vx-col w-full md:w-1/6">
                    <vs-input
                      v-model="exWarningThreshold"
                      class="w-full"
                      disabled
                    />
                  </div>
                  <div class="vx-col  w-full md:w-4/5">
                    <vs-slider
                      v-model="exWarningThreshold"
                      :min="200"
                      :max="1000"
                    />
                  </div>
                </div>
              </vs-tab>
            </template>

            <template v-if="switchs.includes('bdd')">
              <vs-tab label="皮带跑偏检测">
                <p class="text-center">偏移距离</p>
                <div class="vx-row flex mb-5">
                  <div class="vx-col w-full md:w-1/6">
                    <vs-input
                      v-model="offsetDistance"
                      class="w-full"
                      disabled
                    />
                  </div>
                  <div class="vx-col w-full md:w-4/5">
                    <vs-slider v-model="offsetDistance" :min="10" :max="200" />
                  </div>
                </div>
              </vs-tab>
            </template>
          </vs-tabs>
        </template>
        <div class="flex">
          <vs-button type="filled" @click="submitForm" class="mt-10 mx-auto"
            >保存</vs-button
          >
        </div>
      </vx-card>
    </div>

    <!-- preview video -->
    <div class="w-1/2 mt-10">
      <div class="flex">
        <vs-card class="bg-dark w-4/5 mx-auto">
          <div slot="header">
            <h3>预览</h3>
          </div>
          <div slot="media">
            <video
              id="preview_video"
              height="100%"
              width="100%"
              muted
              draggable="false"
            ></video>
          </div>
          <div slot="footer">
            <br />
            <vs-row vs-justify="flex-end">
              <vs-button
                @click="
                  $router
                    .push({
                      name: 'device-camera',
                      params: { camera_id: device.id }
                    })
                    .catch(() => {})
                "
                >刷新</vs-button
              >
            </vs-row>
          </div>
        </vs-card>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Hls from "hls.js";
import { Validator } from "vee-validate";
import zh_CN from "vee-validate/dist/locale/zh_CN";
Validator.localize("zh_CN", zh_CN);
export default {
  data() {
    return {
      test_val: 1,
      device: {
        name: "",
        id: "",
        username: "",
        ip: "",
        passwd: ""
      },
      switchs: [],
      nWarningThreshold: 400,
      exWarningThreshold: 800,
      offsetDistance: 10,
      showTabs: false
    };
  },

  methods: {
    submitForm() {
      const path = "http://localhost:5000/submit";
      const deviceInfo = {
        name: this.device.name,
        username: this.device.username
      };
      this.$validator.validateAll().then(result => {
        if (result) {
          axios.post(path, deviceInfo).then(result => {
            if (result) {
              alert("form submitted!");
            } else {
              alert("Error occored!");
            }
          }).catch((error) => {
          alert(error);
        });
        } else {
          alert("wrong format")
        }
      });
    },

    loadPreviewVideo() {
      if (Hls.isSupported()) {
        const elem = document.getElementById("preview_video");
        this.previw_hls = new Hls();
        this.previw_hls.loadSource(
          "http://ivi.bupt.edu.cn/hls/cctv" + this.test_val + "hd.m3u8"
        );
        this.previw_hls.attachMedia(elem);
        this.previw_hls.on(Hls.Events.MANIFEST_PARSED, () => {
          elem.play(elem);
        });
      }
    },

    destroyPreviewVideo() {
      if (this.previw_hls) {
        this.previw_hls.destroy();
      }
    }
  },

  watch: {
    switchs: function(newVal, oldVal) {
      if (newVal.length && newVal.length < oldVal.length) {
        this.showTabs = false;
        setTimeout(() => {
          this.showTabs = true;
        }, 10);
      } else if (newVal.length) {
        this.showTabs = true;
      } else {
        this.showTabs = false;
      }
    },
    "$route.params.camera_id": function(newVal) {
      this.device.id = newVal;
      this.test_val = 2;
      this.loadPreviewVideo();
    }
  },

  created() {
    this.device.id = this.$route.params.camera_id;
  },

  mounted() {
    this.loadPreviewVideo();
  },

  beforeDestroy() {
    this.destroyPreviewVideo();
  }
};
</script>
