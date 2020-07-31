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
              v-validate="'required'"
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
              v-model="device.password"
              class="w-full mt-10"
            />
            <span class="text-danger text-sm" v-show="errors.has('设备密码')">{{
              errors.first("设备密码")
            }}</span>
          </div>
        </div>
        <div class="vx-row flex mb-10">
          <div class="vx-col w-full md:w-1/2">
            <vs-select v-model="device.location" class="w-full select-large" label="所属矿井">
              <vs-select-item
                :key="loca"
                :value="loca"
                :text="loca"
                v-for="loca in locations"
                class="w-full"
              />
            </vs-select>
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
                      v-model="fodCfg.nWarningThreshold"
                      class="w-full"
                      disabled
                    />
                  </div>
                  <div class="vx-col w-full md:w-4/5">
                    <vs-slider
                      v-model="fodCfg.nWarningThreshold"
                      :min="200"
                      :max="1000"
                    />
                  </div>
                </div>
                <p class="text-center">严重预警阈值</p>
                <div class="vx-row flex">
                  <div class="vx-col w-full md:w-1/6">
                    <vs-input
                      v-model="fodCfg.exWarningThreshold"
                      class="w-full"
                      disabled
                    />
                  </div>
                  <div class="vx-col  w-full md:w-4/5">
                    <vs-slider
                      v-model="fodCfg.exWarningThreshold"
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
                      v-model="bddCfg.offsetDistance"
                      class="w-full"
                      disabled
                    />
                  </div>
                  <div class="vx-col w-full md:w-4/5">
                    <vs-slider
                      v-model="bddCfg.offsetDistance"
                      :min="10"
                      :max="200"
                    />
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
      locations: ["十四采区", "丈八采区", "无"],
      device: {
        name: "",
        id: "",
        username: "",
        ip: "",
        password: "",
        path: "",
        location: ""
      },
      fodCfg: { nWarningThreshold: 400, exWarningThreshold: 800 },
      bddCfg: { offsetDistance: 30 },
      switchs: [],
      showTabs: false
    };
  },

  methods: {
    submitForm() {
      const path = "http://" + process.env.VUE_APP_SERVER_URL + "/apis/device_setting";
      const deviceSetting = {
        device: this.device,
        fodCfg: this.fodCfg,
        bddCfg: this.bddCfg,
        func: this.switchs
      };
      this.$validator.validateAll().then(result => {
        if (result) {
          axios
            .post(path, deviceSetting)
            .then(res => {
              if (res.data.status === "success") {
                alert("保存成功");
              } else {
                alert("保存失败");
              }
            })
            .catch(() => {
              alert("网络错误，保存失败");
            });
        } else {
          alert("请正确填写设置");
        }
      });
    },
    deviceInfoQuery() {
      this.switchs = [];
      this.fodCfg.nWarningThreshold = 400;
      this.fodCfg.exWarningThreshold = 800;
      this.bddCfg.offsetDistance = 30;
      const path = "http://" + process.env.VUE_APP_SERVER_URL + "/apis/device_setting";
      axios
        .get(path, {
          params: {
            device_name: this.device.id
          }
        })
        .then(res => {
          this.device.sourcePath = res.data.device.sourcePath;
          this.device.name = res.data.device.name;
          this.device.username = res.data.device.username;
          this.device.ip = res.data.device.ip;
          this.device.password = res.data.device.password;
          this.device.location = res.data.device.location;
          if (res.data.fodCfg) {
            this.switchs.push("fod");
            this.fodCfg.nWarningThreshold = res.data.fodCfg.nWarningThreshold;
            this.fodCfg.exWarningThreshold = res.data.fodCfg.exWarningThreshold;
          }
          if (res.data.bddCfg) {
            this.switchs.push("bdd");
            this.bddCfg.offsetDistance = res.data.bddCfg.offsetDistance;
          }
        })
        .then(() => {
          this.loadPreviewVideo();
        });
    },

    loadPreviewVideo() {
      if (Hls.isSupported()) {
        const elem = document.getElementById("preview_video");
        this.previw_hls = new Hls();
        this.previw_hls.loadSource(this.device.sourcePath);
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
      this.deviceInfoQuery();
    }
  },

  created() {
    this.device.id = this.$route.params.camera_id;
  },

  mounted() {
    this.deviceInfoQuery();
  },

  beforeDestroy() {
    this.destroyPreviewVideo();
  }
};
</script>
