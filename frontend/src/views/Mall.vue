<template>
  <div class="mall">
    <el-card class="search-card">
      <el-input
        v-model="keyword"
        placeholder="搜索商品"
        clearable
        @clear="loadProducts"
        @keyup.enter="loadProducts"
        style="width: 300px;"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </el-card>

    <div class="products-grid" v-loading="loading">
      <el-card
        v-for="product in products"
        :key="product.id"
        :class="['product-card', { 'blind-box-card': product.is_blind_box }]"
        shadow="hover"
      >
        <div class="product-image">
          <img v-if="product.image_url" :src="product.image_url" :alt="product.name" />
          <div v-else class="no-image">
            <el-icon :size="60" color="#ccc"><Picture /></el-icon>
            <p>暂无图片</p>
          </div>
        </div>

        <div class="product-info">
          <div class="product-tags">
            <el-tag v-if="product.is_blind_box" type="warning" size="small">🎁 盲盒</el-tag>
          </div>
          <h3 class="product-name">{{ product.name }}</h3>
          <p class="product-desc">{{ product.description || '暂无描述' }}</p>

          <div class="product-footer">
            <div class="product-price">
              <span class="price-label">所需能量:</span>
              <span class="price-value">{{ product.points_required }}</span>
            </div>
            <div class="product-stock">
              库存: {{ product.stock }}
            </div>
          </div>

          <el-button
            type="primary"
            :disabled="product.stock === 0 || userStore.userInfo.available_points < product.points_required"
            @click="handleExchange(product)"
            class="exchange-button"
          >
            {{ product.stock === 0 ? '已售罄' : (product.is_blind_box ? '🎁 开盲盒' : '立即兑换') }}
          </el-button>
        </div>
      </el-card>

      <el-empty v-if="!loading && products.length === 0" description="暂无商品" />
    </div>

    <el-pagination
      v-if="total > 0"
      v-model:current-page="page"
      v-model:page-size="pageSize"
      :total="total"
      layout="total, prev, pager, next"
      @current-change="loadProducts"
      class="pagination"
    />

    <el-dialog
      v-model="exchangeDialogVisible"
      :title="selectedProduct ? (selectedProduct.is_blind_box ? `🎁 开启盲盒：${selectedProduct.name}` : `兑换 ${selectedProduct.name}`) : '兑换商品'"
      :width="exchangeDialogWidth"
      destroy-on-close
    >
      <div v-if="selectedProduct" class="exchange-dialog-body">
        <el-alert
          v-if="selectedProduct.is_blind_box"
          title="这是一个神秘盲盒，兑换后将随机获得一个惊喜奖品！"
          type="warning"
          :closable="false"
          show-icon
          style="margin-bottom: 12px;"
        />
        <p class="exchange-info">
          可用能量：<span class="exchange-highlight">{{ userStore.userInfo.available_points }}</span>
        </p>
        <p class="exchange-info">
          单件所需能量：<span class="exchange-highlight">{{ selectedProduct.points_required }}</span>
        </p>
        <p class="exchange-info">
          库存：<span class="exchange-highlight">{{ selectedProduct.stock }}</span>
        </p>
        <el-input-number
          v-model="exchangeQuantity"
          :min="1"
          :max="Math.max(1, maxExchangeQuantity)"
          :disabled="exchangeSubmitting || maxExchangeQuantity === 0"
          controls-position="right"
          class="exchange-quantity"
        />
        <p class="exchange-tip">
          本次最多可兑换 {{ maxExchangeQuantity }} 件
        </p>
      </div>
      <template #footer>
        <el-button :disabled="exchangeSubmitting" @click="exchangeDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          :loading="exchangeSubmitting"
          :disabled="maxExchangeQuantity === 0"
          @click="confirmExchange"
        >
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Search, Picture } from '@element-plus/icons-vue'
import api from '@/utils/api'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const products = ref([])
const loading = ref(false)
const keyword = ref('')
const page = ref(1)
const pageSize = ref(12)
const total = ref(0)
const exchangeDialogVisible = ref(false)
const isMobile = ref(window.innerWidth <= 768)
const handleResize = () => { isMobile.value = window.innerWidth <= 768 }
const exchangeDialogWidth = computed(() => isMobile.value ? '92%' : '420px')
const selectedProduct = ref(null)
const exchangeQuantity = ref(1)
const exchangeSubmitting = ref(false)

const loadProducts = async () => {
  loading.value = true
  try {
    const res = await api.get('/products', {
      params: {
        page: page.value,
        per_page: pageSize.value,
        status: 'on_shelf',
        keyword: keyword.value
      }
    })
    products.value = res.data.list
    total.value = res.data.total
  } catch (error) {
    console.error('加载商品失败:', error)
  } finally {
    loading.value = false
  }
}

const maxExchangeQuantity = computed(() => {
  if (!selectedProduct.value) return 0
  const product = selectedProduct.value
  const stockLimit = Number(product.stock) > 0 ? Number(product.stock) : 0
  const pointsRequired = Number(product.points_required) || 0
  const availablePoints = Number(userStore.userInfo.available_points) || 0
  const pointsLimit = pointsRequired > 0 ? Math.floor(availablePoints / pointsRequired) : stockLimit
  return Math.max(0, Math.min(stockLimit, pointsLimit))
})

const handleExchange = (product) => {
  selectedProduct.value = product
  exchangeQuantity.value = 1
  exchangeDialogVisible.value = true
}

const resetExchangeState = () => {
  selectedProduct.value = null
  exchangeQuantity.value = 1
  exchangeSubmitting.value = false
}

const confirmExchange = async () => {
  if (!selectedProduct.value) return
  if (maxExchangeQuantity.value === 0) {
    ElMessage.warning('当前不能兑换该商品')
    return
  }
  if (exchangeQuantity.value < 1) {
    ElMessage.warning('兑换数量至少为 1 件')
    exchangeQuantity.value = 1
    return
  }
  if (exchangeQuantity.value > maxExchangeQuantity.value) {
    ElMessage.warning(`最多可兑换 ${maxExchangeQuantity.value} 件`)
    exchangeQuantity.value = maxExchangeQuantity.value
    return
  }

  exchangeSubmitting.value = true
  try {
    const res = await api.post('/exchanges', {
      product_id: selectedProduct.value.id,
      quantity: exchangeQuantity.value
    })
    ElMessage.success(res.data.message || '兑换成功')
    exchangeDialogVisible.value = false
    await userStore.getUserInfo()
    await loadProducts()
  } catch (error) {
    console.error('兑换失败:', error)
  } finally {
    exchangeSubmitting.value = false
  }
}

watch(exchangeDialogVisible, (visible) => {
  if (!visible) resetExchangeState()
})

watch(maxExchangeQuantity, (newMax) => {
  if (!exchangeDialogVisible.value) return
  if (newMax > 0 && exchangeQuantity.value > newMax) exchangeQuantity.value = newMax
})

onMounted(() => {
  loadProducts()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.mall {
  max-width: 1400px;
}

.search-card {
  margin-bottom: 24px;
  background: linear-gradient(135deg, #fff0f8 0%, #fff8f0 100%) !important;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  min-height: 400px;
}

.product-card {
  cursor: pointer;
  transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
  display: flex;
  flex-direction: column;
  border-radius: 24px !important;
  overflow: hidden;
}

.product-card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 20px 50px rgba(255, 107, 157, 0.2) !important;
}

.blind-box-card {
  background: linear-gradient(135deg, #fff9f0 0%, #fff3e0 100%) !important;
  box-shadow: 0 8px 30px rgba(255, 170, 0, 0.15) !important;
}

.blind-box-card:hover {
  box-shadow: 0 20px 50px rgba(255, 170, 0, 0.3) !important;
}

@keyframes twinkle {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.08); }
}

.blind-box-card .product-image {
  animation: twinkle 2s ease-in-out infinite;
}

.product-image {
  width: 100%;
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: 16px;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #FFF0F5 0%, #F0F8FF 100%);
}

.product-image img {
  max-width: 100%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.08);
}

.no-image {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #FFF0F5 0%, #F0F8FF 100%);
}

.no-image p {
  margin-top: 10px;
  font-size: 13px;
  color: #ccc;
}

.product-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0 4px;
}

.product-tags {
  margin-bottom: 8px;
  min-height: 24px;
}

.product-name {
  font-size: 18px;
  font-weight: 800;
  margin: 0 0 10px 0;
  color: #333;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-desc {
  font-size: 14px;
  color: #888;
  margin: 0 0 16px 0;
  height: 42px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.5;
}

.product-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.product-price {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.price-label {
  font-size: 13px;
  color: #aaa;
}

.price-value {
  font-size: 24px;
  font-weight: 900;
  color: #FF6B9D;
}

.price-value::before {
  content: '⚡ ';
  font-size: 16px;
}

.product-stock {
  font-size: 13px;
  color: #bbb;
  background: #f5f5f5;
  padding: 2px 10px;
  border-radius: 20px;
}

.exchange-button {
  width: 100%;
  margin-top: auto;
  height: 48px !important;
  font-size: 16px !important;
  font-weight: 800 !important;
  background: linear-gradient(135deg, #FF6B9D 0%, #FF8E53 100%) !important;
  border: none !important;
  color: white !important;
  box-shadow: 0 6px 20px rgba(255, 107, 157, 0.35) !important;
  transition: all 0.3s ease !important;
}

.exchange-button:hover:not(:disabled) {
  transform: translateY(-2px) !important;
  box-shadow: 0 10px 28px rgba(255, 107, 157, 0.5) !important;
  filter: brightness(1.08);
}

.exchange-button:disabled {
  background: linear-gradient(135deg, #ddd 0%, #ccc 100%) !important;
  box-shadow: none !important;
  color: #aaa !important;
}

@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .exchange-button {
    height: 52px !important;
    font-size: 17px !important;
  }

  .product-name {
    font-size: 17px;
    white-space: normal;
  }

  .pagination {
    margin-top: 20px;
  }
}

.exchange-dialog-body {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 8px 0;
}

.exchange-info {
  margin: 0;
  font-size: 15px;
  color: #666;
}

.exchange-highlight {
  color: #FF6B9D;
  font-weight: 700;
  font-size: 17px;
  margin-left: 4px;
}

.exchange-quantity {
  width: 100%;
}

.exchange-tip {
  margin: 0;
  font-size: 13px;
  color: #bbb;
  text-align: center;
}
</style>
