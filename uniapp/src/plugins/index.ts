import { isFunction } from '@vue/shared'
import { App } from 'vue'
import pinia from './/modules/pinia'
import vconsole from './modules/vconsole'
import uview from './modules/uview'
export default {
    install: (app: App) => {
        pinia(app)
        vconsole()
        uview(app)
    }
}
