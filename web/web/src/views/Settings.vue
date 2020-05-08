<template>
  <div class="flex">
    <div class="w-1/2 mx-auto">
      <!-- camera config -->
      <vx-card title="系统配置" class="mb-base mt-10">
        <div class="flex">
          <vs-button
            type="filled"
            @click="systemReboot"
            class="mt-10 mx-auto"
            >重启系统</vs-button
          >
        </div>
      </vx-card>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { Validator } from "vee-validate";
import zh_CN from "vee-validate/dist/locale/zh_CN";
Validator.localize("zh_CN", zh_CN);
export default {
  data() {
    return {};
  },

  methods: {
    systemReboot() {
      const path = "http://192.168.20.25:8081/system_setting";
      axios.post(path, "Reboot").then(result => {
        if (result) {
          alert("form submitted!");
        } else {
          alert("Error occored!");
        }
      });
    }
  }
};
</script>
