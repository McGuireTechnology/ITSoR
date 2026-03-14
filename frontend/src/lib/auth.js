const TOKEN_KEY = 'itsor_access_token'

export function getToken() {
  return window.localStorage.getItem(TOKEN_KEY)
}

export function setToken(token) {
  window.localStorage.setItem(TOKEN_KEY, token)
  window.dispatchEvent(new Event('itsor-auth-changed'))
}

export function clearToken() {
  window.localStorage.removeItem(TOKEN_KEY)
  window.dispatchEvent(new Event('itsor-auth-changed'))
}

function decodeBase64Url(input) {
  const normalized = input.replace(/-/g, '+').replace(/_/g, '/')
  const padded = normalized.padEnd(normalized.length + ((4 - (normalized.length % 4)) % 4), '=')
  return atob(padded)
}

function getTokenPayload(token) {
  if (!token) {
    return null
  }

  const parts = token.split('.')
  if (parts.length < 2) {
    return null
  }

  try {
    return JSON.parse(decodeBase64Url(parts[1]))
  } catch {
    return null
  }
}

export function getTokenSubject(token) {
  const payload = getTokenPayload(token)
  return typeof payload?.sub === 'string' ? payload.sub : null
}

export function hasValidToken() {
  const token = getToken()
  if (!token) {
    return false
  }

  const payload = getTokenPayload(token)
  if (!payload || typeof payload.sub !== 'string') {
    return false
  }

  if (typeof payload.exp !== 'number') {
    return true
  }

  const nowInSeconds = Math.floor(Date.now() / 1000)
  return payload.exp > nowInSeconds
}
