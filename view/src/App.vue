<template lang="pug">
  v-app
    v-container(fluid)
      v-layout(row wrap)
        v-flex(v-for="ero, index in eroiines")
          v-layout()
            v-flex#twitter-card.ma-3
              tweet(:id="index" :options="{ width: 300 }")
                
</template>

<script lang='ts'>
import { Component, Vue } from 'vue-property-decorator';
// import { Observable } from 'rxjs';
import axios from 'axios';
import { Tweet } from 'vue-tweet-embed';
            //tweet(:id="index")

@Component({
  components: {
    Tweet
  },
})
export default class App extends Vue {
  private eroiines = {};
  private mounted() {
    axios.get('http://localhost:5000')
      .then(
        (response) => {
          this.eroiines = response.data;
          console.log(response.data);
        },
    );
  }
}
</script>

<style lang="stylus" scoped>
#twitter-card
  width: 250px;

</style>

