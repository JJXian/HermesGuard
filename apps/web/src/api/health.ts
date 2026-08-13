export type DependencyState = 'up' | 'down'

export interface ReadyResponse {
  status: 'ready' | 'not_ready'
  dependencies: {
    mysql: DependencyState
    redis: DependencyState
  }
}

export async function fetchReadiness(): Promise<ReadyResponse> {
  const response = await fetch('/api/health/ready')
  const data = (await response.json()) as ReadyResponse

  if (!response.ok && response.status !== 503) {
    throw new Error(`健康检查请求失败：${response.status}`)
  }

  return data
}
