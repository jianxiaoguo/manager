<!--用户菜单-->
<template>
<div :id="'vue-content-'+Math.random().toString(36).substring(2)">
    <span v-if="unreadCount > 0" class="bell-badge"></span>
    <a class="glostick__menu-icon glostick__menu-icon--account" @click="openOrCloseMenu">
        <div class="glostick__user__avatar--container">
            <img class="glostick__user__avatar" :src="'/v1/avatar/' + user.username" id="menu-account">
        </div>
        <div class="glostick__user__notification "></div>
    </a>
    <ul id="glostick__menu--account" class="glostick__menu glostick__menu--account" :class="{'glostick__menu--open': isMenuActived}">
        <li class="glostick__menu__listitem">
            <a class="glostick__menu__item glostick__menu__item--account-details" href="/account">
                <div class="glostick__user__avatar--container">
                    <img class="glostick__account-details__avatar" :src="'/v1/avatar/' + user.username" >
                </div>
                <div v-if="user.first_name || user.last_name" class="glostick__account-details__name">
                  {{user.first_name}} {{user.last_name}}
                </div>
                <div v-else class="glostick__account-details__name">
                  {{user.username}}
                </div>
                <div class="glostick__account-details__email">
                  {{user.email}}
                </div>
            </a>
        </li>
        <li class="glostick__menu__listitem">
            <a class="glostick__menu__item glostick__menu__item--settings" href="/account">Account settings</a>
        </li>

        <li class="glostick__menu__listitem">
            <div v-if="unreadCount > 0" class="bell-badge-count">{{unreadCount}}</div>
            <a class="glostick__menu__item glostick__menu__item--notifications" href="/notifications">Notifications</a>
        </li>
        <li class="glostick__menu__listitem">
            <a class="glostick__menu__item glostick__menu__item--signout" @click="logout">Sign out</a>
        </li>
    </ul>
</div>
</template>

<script>
import UserMenu from "./UserMenu"
export default UserMenu
</script>

<style scoped>
    .bell-badge {
        position: absolute;
        right: 8px;
        top: 8px;
        z-index: 2;
        width: 14px;
        height: 14px;
        color: #fff;
        background: #ff5353;
        background-clip: padding-box;
        border: 2px solid transparent;
        border-color: transparent;
        border-color: rgba(0,0,0,0);
        border-radius: 50%;
    }

    .bell-badge-count {
        margin-left: 200px;
        margin-top: 10px;
        z-index: 999;
        position:absolute;
        min-width: 18px;
        min-height: 18px;
        padding: 0 5px;
        line-height: 18px;
        text-align: center;
        border-radius: 500rem;
        color: #fff;
        font-weight: 600;
        background: #ff5353;
        
        font-family: SFProText-Heavy,'Helvetica Neue',Arial,Helvetica,sans-serif
    }


    .glostick__menu--account {
        top: 42px
    }
</style>
