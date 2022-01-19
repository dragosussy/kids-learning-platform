<template>
  <div class="admin-view">
    <div class="centered">
      <div>
        <p><b>Select Date:</b></p>
        <Datepicker
          v-model="selectedDate"
          :format="dateTimeFormatter"
        ></Datepicker>
      </div>

      <div>
        <p><b>Select User:</b></p>
        <select v-model="selectedUser" @change="populateChart">
          <option v-for="user in allUsers" :key="user.id">
            {{ user.name + " " + user.surname }}
          </option>
        </select>
      </div>
    </div>

    <div>
      <apexchart
        width="900"
        type="line"
        ref="chart"
        :options="chartOptions"
        :series="series"
      ></apexchart>
    </div>
  </div>
</template>

<script>
import Datepicker from "vuejs-datepicker";

export default {
  components: {
    Datepicker,
  },
  data: function () {
    return {
      getEmotionsDataUrl: "https://localhost:44373/data/daily-report/",
      getAllUsersUrl: "https://localhost:44373/data/all-users/",
      selectedUser: null,
      selectedDate: null,
      allUsers: [],
      chartOptions: {
        chart: {
          id: "vuechart-example",
        },
        xaxis: {
          type: "datetime",
          categories: [],
        },
        yaxis: {
          tickAmount: 6,
          labels: {
            formatter: function (val) {
              if (val == 0) return "Disgust";
              if (val == 1) return "Angry";
              if (val == 2) return "Fear";
              if (val == 3) return "Sadness";
              if (val == 4) return "Neutral";
              if (val == 5) return "Surprise";
              if (val == 6) return "Happiness";
              return val;
            },
          },
        },
      },
      series: [
        {
          name: "Emotion",
          data: [],
        },
      ],
    };
  },
  mounted() {
    fetch(this.getAllUsersUrl, {
      method: "GET",
      mode: "cors",
    })
      .then((response) => response.json())
      .then((usersArray) => {
        this.allUsers = usersArray;
      });
  },
  methods: {
    dateTimeFormatter(date) {
      let x = this.$moment(date).format("MM/DD/YYYY, h:mm:ss a");
      console.log(x);
      return x;
    },
    getEmotionCode(emotionString) {
      if (emotionString == "Disgust") return 0;
      if (emotionString == "Angry") return 1;
      if (emotionString == "Fear") return 2;
      if (emotionString == "Sad") return 3;
      if (emotionString == "Neutral") return 4;
      if (emotionString == "Surprise") return 5;
      if (emotionString == "Happy") return 6;
    },
    populateChart() {
      fetch(
        `${this.getEmotionsDataUrl}?date=${this.dateTimeFormatter(
          this.selectedDate
        )}&username=${this.selectedUser}`,
        {
          method: "GET",
          mode: "cors",
        }
      )
        .then((response) => response.json())
        .then((emotionsDictionary) => {
          let newCategsArray = [];
          for (let key in emotionsDictionary.emotions) {
            newCategsArray.push(key);
            this.series[0].data.push(
              this.getEmotionCode(emotionsDictionary.emotions[key])
            );
          }

          this.$refs.chart.updateOptions({
            xaxis: { categories: newCategsArray },
          });
          console.log(this.chartOptions.xaxis.categories);
          console.log(this.series[0].data);
        });
    },
  },
};
</script>


<style>
body {
  background-color: #55666b;
}
.centered {
  align-items: center;
  display: flex;
}
</style>