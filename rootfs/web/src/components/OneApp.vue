<!--单个app显示-->
<template>
    <a @click="goToAppDetail()" class="ember-view link cursor-hand dark-gray">
        <div class="flex items-baseline limit-width">
            <div class="relative w3 mr1 ember-view">
                <icon-application-one size="2rem" class="icon malibu-icon v-mid malibu-fill-gradient-bule o-60" fill="#409EFF"/>
            </div>
            <span class="f3 dark-gray"> {{name}} </span>
            <div class="flex-auto"></div>
            <ol class="f5 flex list mv0 pa0 items-center">
                <li class="mr1 db-l dn">
                    <a href="/apps/zmy/settings" class="link dark-gray flex ember-view">
                        <span class="mr1 nudge-up--2 o-80">
                            <svg style="height: 16px; width: 16px;" class="icon malibu-icon malibu-fill-gradient-dark-gray">
                                <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#language-python-16"></use>
                            </svg>
                        </span>
                    </a>
                </li>
                <li><span class="gray db-l dn">•</span></li>
                <li class="mh1 items-center flex-l dn">
<!--                    <a href="/apps/zmy/settings" class="link dark-gray ember-view">-->
<!--                        {{baseImage}}-->
<!--                    </a>-->
                </li>
                <li><span class="gray db-l dn">•</span></li>
<!--                <li class="mh1 db-l dn">-->
<!--                    <a href="/apps/zmy/settings" class="link dark-gray ember-view">-->
<!--                        Europe-->
<!--                    </a>-->
<!--                </li>-->

                <li class="ml2 flex items-center">
                    <button class="nudge-up--1 cursor-pointer b--0 bg-transparent b--transparent pa1 ember-view">
                        <svg style="height: 16px; width: 16px;" class="icon malibu-icon fill-gray">
                            <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#favorite-option-16"></use>
                        </svg>
                    </button>
                </li>
            </ol>
        </div>
    </a>
</template>

<script>
import OneApp from "./OneApp"
export default OneApp
</script>

<style scoped>
    /*@import "../assets/bashboard. ";*/
</style>
