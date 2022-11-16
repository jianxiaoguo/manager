<!--导航栏菜单组件-->
<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <a role="button" class="glostick__menu-icon" @click="openOrCloseMenu">
        <div class="icon-navigator-toggle" id="menu-nav"></div>
    </a>
    <ul id="glostick__menu--navigator" class="glostick__menu glostick__menu--navigator" :class="{'glostick__menu--open': isMenuActived}">
        <li class="glostick__menu__listitem">
            <a class="glostick__menu__item glostick__menu__item--dashboard" href="/">Dashboard</a>
        </li>
        <li class="glostick__menu__listitem">
            <a class="glostick__menu__item glostick__menu__item--elements" href="/pricing">Drycc Pricing</a>
        </li>
        <li class="glostick__menu__listitem">
            <a class="glostick__menu__item glostick__menu__item--support" target="_blank" href="https://tawk.to/chat/6234b5491ffac05b1d7f4669/1fueu8a9t">Contact Us</a>
        </li>
        <li class="glostick__menu__listitem">
            <a class="glostick__menu__item glostick__menu__item--docs" target="_blank" href="https://www.drycc.cc">Documentation</a>
        </li>
    </ul>
</div>
</template>

<script>
import NavMenu from "./NavMenu"
export default NavMenu
</script>

<style scoped>
    .glostick__menu--navigator {
        top: 42px
    }
</style>
