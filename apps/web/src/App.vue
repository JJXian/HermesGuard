<script setup lang="ts">
import { Connection, DataBoard, Refresh } from '@element-plus/icons-vue'
import { ElAlert, ElButton, ElIcon, ElTag } from 'element-plus'
import 'element-plus/es/components/alert/style/css'
import 'element-plus/es/components/button/style/css'
import 'element-plus/es/components/icon/style/css'
import 'element-plus/es/components/tag/style/css'
import { computed, onMounted, ref } from 'vue'

import { fetchReadiness, type ReadyResponse } from './api/health'

const readiness = ref<ReadyResponse | null>(null)
const loading = ref(false)
const errorMessage = ref('')

const overallStatus = computed(() => {
  if (errorMessage.value) return '无法连接'
  if (!readiness.value) return '检查中'
  return readiness.value.status === 'ready' ? '运行正常' : '依赖未就绪'
})

const overallType = computed(() => {
  if (errorMessage.value) return 'danger'
  return readiness.value?.status === 'ready' ? 'success' : 'warning'
})

async function refreshHealth(): Promise<void> {
  loading.value = true
  errorMessage.value = ''
  try {
    readiness.value = await fetchReadiness()
  } catch (error) {
    readiness.value = null
    errorMessage.value = error instanceof Error ? error.message : '未知连接错误'
  } finally {
    loading.value = false
  }
}

onMounted(refreshHealth)
</script>

<template>
  <main class="page-shell">
    <section class="hero-panel">
      <div class="brand-mark">
        HG
      </div>
      <div>
        <p class="eyebrow">
          电商智能巡检平台
        </p>
        <h1>HermesGuard</h1>
        <p class="subtitle">
          规则负责确认事实，Agent 负责解释上下文。当前页面用于验证阶段 1 的系统基础设施。
        </p>
      </div>
    </section>

    <section class="status-panel">
      <div class="section-heading">
        <div>
          <p class="eyebrow">
            SYSTEM STATUS
          </p>
          <h2>服务运行状态</h2>
        </div>
        <el-button :icon="Refresh" :loading="loading" @click="refreshHealth">
          重新检查
        </el-button>
      </div>

      <el-alert
        v-if="errorMessage"
        :title="errorMessage"
        type="error"
        show-icon
        :closable="false"
      />

      <div class="status-grid">
        <article class="status-card status-card--primary">
          <el-icon><Connection /></el-icon>
          <div>
            <span>HermesGuard API</span>
            <strong>{{ overallStatus }}</strong>
          </div>
          <el-tag :type="overallType" effect="dark">
            {{ readiness?.status ?? 'unknown' }}
          </el-tag>
        </article>

        <article class="status-card">
          <el-icon><DataBoard /></el-icon>
          <div>
            <span>MySQL</span>
            <strong>{{ readiness?.dependencies.mysql === 'up' ? '连接正常' : '等待连接' }}</strong>
          </div>
          <span class="status-dot" :class="{ active: readiness?.dependencies.mysql === 'up' }" />
        </article>

        <article class="status-card">
          <el-icon><DataBoard /></el-icon>
          <div>
            <span>Redis</span>
            <strong>{{ readiness?.dependencies.redis === 'up' ? '连接正常' : '等待连接' }}</strong>
          </div>
          <span class="status-dot" :class="{ active: readiness?.dependencies.redis === 'up' }" />
        </article>
      </div>
    </section>
  </main>
</template>
