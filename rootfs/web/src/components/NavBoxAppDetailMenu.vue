<template>
    <div>
        <div class="flex items-center">
            <button class="nudge-up--1 cursor-pointer b--0 bg-transparent b--transparent pa1 ember-view">
                <svg style="height: 16px; width: 16px;" class="icon malibu-icon fill-gray">
                    <use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#favorite-option-16"></use>
                </svg>
            </button>
            <a v-bind:href="domain" title="Open Application" target="_blank" class="hk-button--secondary ml3 open-app-button bule">
                Open app
            </a>
            <div class="ember-view">
                <span class="confirmable-action ember-view"></span>
            </div>
        </div>
    </div>
</template>

<script>
import NavBoxAppDetailMenu from "./NavBoxAppDetailMenu"
export default NavBoxAppDetailMenu
</script>

<style scoped>

</style>
