<template>
  <div class="broadcast-settings">
    <div class="page-header">
      <h2>📡 星际广播台</h2>
      <p class="subtitle">配置局域网音箱连接与自动播报规则</p>
    </div>

    <el-row :gutter="24">
      <!-- 左列：连接设置 + 即时播报 -->
      <el-col :xs="24" :md="12">
        <!-- 音箱连接 -->
        <el-card class="setting-card" shadow="never">
          <template #header>
            <div class="card-header">
              <el-icon><Connection /></el-icon>
              <span>音箱连接配置</span>
            </div>
          </template>

          <el-form :model="form" label-position="top" class="setting-form">
            <el-form-item label="音箱 IP 地址">
              <el-input
                v-model="form.speaker_ip"
                placeholder="例：192.168.1.10"
                clearable
              >
                <template #prefix><el-icon><Monitor /></el-icon></template>
              </el-input>
            </el-form-item>

            <el-form-item label="音箱端口">
              <el-input-number
                v-model="form.speaker_port"
                :min="1"
                :max="65535"
                style="width: 100%"
              />
              <div class="form-tip">WebSocket 服务端口，默认 18888</div>
            </el-form-item>

            <el-form-item label="心跳间隔（秒）">
              <el-input-number
                v-model="form.heartbeat_interval"
                :min="1"
                :max="120"
                style="width: 100%"
              />
              <div class="form-tip">保持连接的心跳频率，默认 10 秒</div>
            </el-form-item>
          </el-form>

          <el-button
            type="primary"
            plain
            round
            :loading="testLoading"
            @click="handleTestBroadcast"
            style="width: 100%"
          >
            <el-icon><Mic /></el-icon>
            发送测试广播
          </el-button>
        </el-card>

        <!-- 即时播报开关 -->
        <el-card class="setting-card" shadow="never" style="margin-top: 20px">
          <template #header>
            <div class="card-header">
              <el-icon><Bell /></el-icon>
              <span>即时发分播报</span>
            </div>
          </template>

          <div class="switch-row">
            <div class="switch-label">
              <div class="switch-title">全局即时播报开关</div>
              <div class="switch-desc">管理员手动发分或审批任务时，自动向音箱播报获奖消息</div>
            </div>
            <el-switch v-model="form.enable_broadcast" active-color="#7B68EE" />
          </div>
        </el-card>
      </el-col>

      <!-- 右列：定时简报 -->
      <el-col :xs="24" :md="12">
        <el-card class="setting-card" shadow="never">
          <template #header>
            <div class="card-header">
              <el-icon><AlarmClock /></el-icon>
              <span>定时星际简报</span>
            </div>
          </template>

          <el-form :model="form" label-position="top" class="setting-form">
            <el-form-item>
              <div class="switch-row" style="margin-bottom: 0">
                <div class="switch-label">
                  <div class="switch-title">启用每日定时简报</div>
                  <div class="switch-desc">按设定时间自动播报能量概况与心愿追踪</div>
                </div>
                <el-switch v-model="form.enable_timed_broadcast" active-color="#7B68EE" />
              </div>
            </el-form-item>

            <el-form-item label="早上简报时间">
              <el-time-picker
                v-model="morningTime"
                format="HH:mm"
                value-format="HH:mm"
                placeholder="选择早上播报时间"
                :disabled="!form.enable_timed_broadcast"
                style="width: 100%"
              />
            </el-form-item>

            <el-form-item label="晚上简报时间">
              <el-time-picker
                v-model="eveningTime"
                format="HH:mm"
                value-format="HH:mm"
                placeholder="选择晚上播报时间"
                :disabled="!form.enable_timed_broadcast"
                style="width: 100%"
              />
            </el-form-item>

            <el-form-item label="播报目标宇航员">
              <el-select
                v-model="form.broadcast_targets"
                multiple
                clearable
                placeholder="留空则播报全部宇航员"
                :disabled="!form.enable_timed_broadcast"
                style="width: 100%"
              >
                <el-option
                  v-for="user in userList"
                  :key="user.id"
                  :label="user.real_name"
                  :value="user.id"
                />
              </el-select>
              <div class="form-tip">未选择时默认向所有宇航员播报</div>
            </el-form-item>
          </el-form>

          <!-- 模板预览 -->
          <el-collapse class="template-preview">
            <el-collapse-item name="morning">
              <template #title>
                <span class="preview-title">早晨简报预览</span>
              </template>
              <div class="preview-text">
                早上好，小宇航员 <strong>[姓名]</strong>！新一天的星际航行开始啦！目前飞船总能量为 <strong>[N]</strong> 个星辰币。昨天的表现非常棒，今天也要继续加油巡航哦！<em>（若有心愿）</em>星际雷达提示，距离你的心愿目标【<strong>[心愿名]</strong>】，只差最后 <strong>[M]</strong> 个星辰币啦，一鼓作气拿下它吧！
              </div>
            </el-collapse-item>
            <el-collapse-item name="evening">
              <template #title>
                <span class="preview-title">晚间简报预览</span>
              </template>
              <div class="preview-text">
                夜幕降临，空间站广播开启。小宇航员 <strong>[姓名]</strong>，今天的航行辛苦啦！目前总能量为 <strong>[N]</strong> 个星辰币。快快开启睡眠舱模式，恢复体力，明天见！<em>（若有心愿）</em>悄悄告诉你，再积攒 <strong>[M]</strong> 个星辰币，就能成功解锁【<strong>[心愿名]</strong>】了哦，继续努力！
              </div>
            </el-collapse-item>
          </el-collapse>
        </el-card>
      </el-col>
    </el-row>

    <!-- 保存按钮 -->
    <div class="save-bar">
      <el-button
        type="primary"
        size="large"
        round
        :loading="saveLoading"
        @click="handleSave"
      >
        保存配置
      </el-button>
      <el-button size="large" round @click="handleReset">重置</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Connection, Bell, AlarmClock, Mic, Monitor } from '@element-plus/icons-vue'
import api from '@/utils/api'

const saveLoading = ref(false)
const testLoading = ref(false)
const userList = ref([])

const form = ref({
  speaker_ip: '',
  speaker_port: 18888,
  heartbeat_interval: 10,
  enable_broadcast: false,
  enable_timed_broadcast: false,
  morning_broadcast_time: '07:00',
  evening_broadcast_time: '21:00',
  broadcast_targets: []
})

// el-time-picker 绑定：字符串 "HH:mm"
const morningTime = computed({
  get: () => form.value.morning_broadcast_time || '07:00',
  set: (val) => { form.value.morning_broadcast_time = val || '07:00' }
})

const eveningTime = computed({
  get: () => form.value.evening_broadcast_time || '21:00',
  set: (val) => { form.value.evening_broadcast_time = val || '21:00' }
})

const originalForm = ref({})

const fetchSettings = async () => {
  try {
    const res = await api.get('/settings')
    if (res.code === 200) {
      Object.assign(form.value, res.data)
      originalForm.value = JSON.parse(JSON.stringify(res.data))
    }
  } catch {
    ElMessage.error('加载配置失败')
  }
}

const fetchUsers = async () => {
  try {
    const res = await api.get('/users', { params: { role: 'user', per_page: 200 } })
    if (res.code === 200) {
      userList.value = res.data.list || []
    }
  } catch {
    // 静默处理
  }
}

const handleSave = async () => {
  saveLoading.value = true
  try {
    const res = await api.put('/settings', form.value)
    if (res.code === 200) {
      ElMessage.success('配置已保存，定时任务已更新')
      originalForm.value = JSON.parse(JSON.stringify(form.value))
    } else {
      ElMessage.error(res.message || '保存失败')
    }
  } catch {
    ElMessage.error('保存失败，请检查网络')
  } finally {
    saveLoading.value = false
  }
}

const handleReset = () => {
  Object.assign(form.value, JSON.parse(JSON.stringify(originalForm.value)))
}

const handleTestBroadcast = async () => {
  if (!form.value.speaker_ip) {
    ElMessage.warning('请先填写音箱 IP 地址并保存')
    return
  }
  testLoading.value = true
  try {
    const res = await api.post('/settings/test-broadcast')
    if (res.code === 200) {
      ElMessage.success('测试广播已发送，请留意音箱是否有声音')
    } else {
      ElMessage.error(res.message || '发送失败')
    }
  } catch {
    ElMessage.error('音箱未连接，请检查 IP 和网络')
  } finally {
    testLoading.value = false
  }
}

onMounted(() => {
  fetchSettings()
  fetchUsers()
})
</script>

<style scoped>
.broadcast-settings {
  max-width: 960px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 28px;
}

.page-header h2 {
  font-size: 22px;
  font-weight: 900;
  color: #333;
  margin: 0 0 6px;
}

.subtitle {
  color: #888;
  font-size: 14px;
  margin: 0;
}

.setting-card {
  border-radius: 16px;
  border: 1.5px solid #f0ebff;
}

.setting-card :deep(.el-card__header) {
  background: linear-gradient(135deg, #f8f5ff, #fff);
  border-bottom: 1px solid #f0ebff;
  padding: 14px 20px;
  border-radius: 16px 16px 0 0;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 700;
  color: #7B68EE;
  font-size: 15px;
}

.setting-form {
  margin-bottom: 4px;
}

.form-tip {
  font-size: 12px;
  color: #bbb;
  margin-top: 4px;
}

.switch-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 4px 0;
}

.switch-label { flex: 1; }

.switch-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.switch-desc {
  font-size: 12px;
  color: #999;
  line-height: 1.5;
}

.template-preview {
  margin-top: 8px;
  border-radius: 10px;
  overflow: hidden;
}

.template-preview :deep(.el-collapse-item__header) {
  background: #faf8ff;
  padding: 0 12px;
  font-size: 13px;
  color: #7B68EE;
}

.preview-title {
  font-weight: 600;
}

.preview-text {
  font-size: 13px;
  color: #555;
  line-height: 1.8;
  padding: 8px 12px;
  background: #fdfcff;
  border-radius: 8px;
}

.preview-text em {
  color: #bbb;
  font-style: normal;
}

.save-bar {
  margin-top: 28px;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-bottom: 24px;
}
</style>
