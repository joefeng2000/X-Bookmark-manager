// frontend/src/lib/errorHandler.ts

/**
 * 类型守卫：检查是否是对象
 */
function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null;
}

/**
 * 类型守卫：检查对象是否有指定属性
 */
function hasProperty<K extends string>(
  obj: unknown,
  key: K
): obj is Record<K, unknown> {
  return isObject(obj) && key in obj;
}

/**
 * 类型守卫：检查是否是标准Error对象
 */
function isErrorInstance(error: unknown): error is Error {
  return error instanceof Error;
}

/**
 * 类型守卫：检查是否是axios风格的错误
 */
function isAxiosError(error: unknown): error is {
  response?: {
    data?: {
      detail?: unknown;
      message?: unknown;
    };
    status?: number;
  };
  message?: unknown;
} {
  return (
    isObject(error) &&
    hasProperty(error, "response") &&
    (error.response === undefined || isObject(error.response))
  );
}

/**
 * 从各种类型的错误对象中提取错误消息
 */
export function getErrorMessage(error: unknown): string {
  // 检查是否是标准Error对象
  if (isErrorInstance(error)) {
    return error.message;
  }

  // 检查是否是axios错误（或类似结构）
  if (isAxiosError(error) && error.response) {
    const response = error.response;

    // 尝试从response.data.detail获取
    if (
      isObject(response.data) &&
      hasProperty(response.data, "detail") &&
      typeof response.data.detail === "string"
    ) {
      return response.data.detail;
    }

    // 尝试从response.data.message获取
    if (
      isObject(response.data) &&
      hasProperty(response.data, "message") &&
      typeof response.data.message === "string"
    ) {
      return response.data.message;
    }
  }

  // 检查是否有message属性（通用错误对象）
  if (hasProperty(error, "message") && typeof error.message === "string") {
    return error.message;
  }

  // 如果是字符串，直接返回
  if (typeof error === "string") {
    return error;
  }

  // 其他情况返回通用错误
  return "发生未知错误";
}

/**
 * 检查是否是网络错误
 */
export function isNetworkError(error: unknown): boolean {
  if (isAxiosError(error) && error.response) {
    const status = error.response.status;
    return typeof status === "number" && (status >= 500 || status === 0);
  }

  if (hasProperty(error, "message") && typeof error.message === "string") {
    return error.message.toLowerCase().includes("network");
  }

  return false;
}

/**
 * 检查是否是认证错误
 */
export function isAuthError(error: unknown): boolean {
  if (isAxiosError(error) && error.response) {
    const status = error.response.status;
    return status === 401 || status === 403;
  }
  return false;
}
