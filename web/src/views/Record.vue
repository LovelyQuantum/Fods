<template>
  <vx-card>
    <vs-table @selected="handleSelected" v-model="selected" :data="users">
      <template slot="header">
        <div>
          <h2>预警记录</h2>
          <div class="vx-row mb-1 mt-5">
            <div class="my-auto ml-5 mr-5"><span>范围查询</span></div>
            <datepicker
              :language="zh"
              :format="dateFormat"
              placeholder="起始日期"
              v-model="dateRangeBegin"
              class="my-auto"
            ></datepicker>
            <div class="my-auto ml-5 mr-5"><span>—</span></div>
            <datepicker
              :language="zh"
              :format="dateFormat"
              placeholder="截至日期"
              v-model="dateRangeEnd"
              class="my-auto"
            ></datepicker>
            <vs-button
              color="primary"
              type="filled"
              class="ml-5"
              @click="recordQuery()"
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
          <div class="vx-row mb-5">
            <p class="ml-10" v-if="recordQueryMessage">
              {{ recordQueryMessage }}
            </p>
          </div>
        </div>
      </template>
      <template slot="thead">
        <vs-th>Email</vs-th>
        <vs-th>Name</vs-th>
        <vs-th>Website</vs-th>
        <vs-th>Nro</vs-th>
      </template>

      <template slot-scope="{ data }">
        <vs-tr :data="tr" :key="indextr" v-for="(tr, indextr) in data">
          <vs-td :data="data[indextr].email">
            {{ data[indextr].email }}
          </vs-td>
          <vs-td :data="data[indextr].username">
            {{ data[indextr].username }}
          </vs-td>
          <vs-td :data="data[indextr].id">
            {{ data[indextr].website }}
          </vs-td>
          <vs-td :data="data[indextr].id">
            {{ data[indextr].id }}
          </vs-td>
        </vs-tr>
      </template>
    </vs-table>
    <vs-pagination :total="400" v-model="currentx" class="mt-10"></vs-pagination>
    <vs-popup
      class="holamundo"
      title="Lorem ipsum dolor sit amet"
      :active.sync="previewPopupActive"
    >
      <p>
        Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
        tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim
        veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea
        commodo consequat.
      </p>
    </vs-popup>
  </vx-card>
</template>

<script>
import Datepicker from "vuejs-datepicker";
import { zh } from "vuejs-datepicker/dist/locale";

export default {
  components: {
    Datepicker
  },
  data() {
    return {
      zh: zh,
      dateFormat: "yyyy-MM-dd",
      selected: null,
      activeLine: null,
      dateRangeBegin: null,
      dateRangeEnd: null,
      recordQueryMessage: null,
      log: [],
      currentx: 14,
      previewPopupActive: false,
      users: [
        {
          id: 1,
          name: "Leanne Graham",
          username: "Bret",
          email: "Sincere@april.biz",
          website: "hildegard.org"
        },
        {
          id: 2,
          name: "Ervin Howell",
          username: "Antonette",
          email: "Shanna@melissa.tv",
          website: "anastasia.net"
        },
        {
          id: 3,
          name: "Clementine Bauch",
          username: "Samantha",
          email: "Nathan@yesenia.net",
          website: "ramiro.info"
        },
        {
          id: 4,
          name: "Patricia Lebsack",
          username: "Karianne",
          email: "Julianne.OConner@kory.org",
          website: "kale.biz"
        },
        {
          id: 5,
          name: "Chelsey Dietrich",
          username: "Kamren",
          email: "Lucio_Hettinger@annie.ca",
          website: "demarco.info"
        },
        {
          id: 6,
          name: "Mrs. Dennis Schulist",
          username: "Leopoldo_Corkery",
          email: "Karley_Dach@jasper.info",
          website: "ola.org"
        },
        {
          id: 7,
          name: "Kurtis Weissnat",
          username: "Elwyn.Skiles",
          email: "Telly.Hoeger@billy.biz",
          website: "elvis.io"
        }
      ]
    };
  },
  methods: {
    clearDateRange() {
      this.dateRangeBegin = null;
      this.dateRangeEnd = null;
      this.recordQueryMessage = null;
    },

    recordQuery() {
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
      } else {
        this.recordQueryMessage = null;
      }
    },
    handleChangePage(page) {
      console.log(`The user changed the page to: ${page}`);
    },
    handleSelected(tr) {
      if (this.activeLine === tr) {
        this.selected = null;
        this.activeLine = null;
      } else {
        this.activeLine = tr;
        this.previewPopupActive = true;
      }
    }
  },
  watch: {
    currentx: (newVal, oldVal) => {
      console.log("page change from " + oldVal + " to " + newVal);
    }
  }
};
</script>
