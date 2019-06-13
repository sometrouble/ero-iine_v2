<template lang="pug">
  v-app(fluid)
    v-container(fluid)
      v-layout(justify-center row wrap)
        v-flex(v-for="ero, index in eroiines")
          v-card#twitter-card.mt-3
            v-layout(row)
              v-flex(xs6)
                v-img(:src="ero.image_url1" style="width:170px; height:170px; object-fit:cover;")
              v-flex(xs6)
                article.pa-1
                  p {{ index }}
                  v-img(:src="require('@/assets/images/twitter.png')" width="24" height="24" style="position:absolute; bottom: 0; right:0;")
                
</template>

<script lang='ts'>
import { Component, Vue } from 'vue-property-decorator';
// import { Observable } from 'rxjs';
import axios from 'axios';
//import { Tweet } from 'vue-tweet-embed';
            //tweet(:id="index")

@Component({
  components: {
    //Tweet
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
  width: 340px;
  height: 170px;
</style>

