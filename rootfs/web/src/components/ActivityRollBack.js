// import { useRouter } from 'vue-router'
import { reactive, toRefs } from 'vue'

export default {
    name: "ActivityRollBack",
    props: {
        appDetail: [Object, Function],
        rollBackIndex: 0,
        activities: Array
    },
    setup(props, context) {

        const state = reactive({
            rollActivities: props.activities.slice(0, props.rollBackIndex),
            currentActivity: props.activities[props.rollBackIndex]
        })

        const closeRollBack = () => {
            context.emit('closeRB')
        }

        const rollBack = () => {
            context.emit('closeRB')
        }

        return {
            ...toRefs(state),
            closeRollBack,
            rollBack
        }

    }
}
