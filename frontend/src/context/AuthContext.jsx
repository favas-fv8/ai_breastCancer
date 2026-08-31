import { createContext, useCallback, useContext, useEffect, useState } from "react";
import {
  apiPost,
  apiGet,
  getUser,
  setAuth,
  setStoredUser,
  clearAuth,
  isAuthenticated,
} from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(getUser);
  const [loading, setLoading] = useState(false);

  const refreshProfile = useCallback(async () => {
    try {
      const data = await apiGet("/auth/profile/");
      setUser(data);
      setStoredUser(data);
    } catch {
      // If the token is invalid, force logout.
      clearAuth();
      setUser(null);
    }
  }, []);

  useEffect(() => {
    if (isAuthenticated()) {
      refreshProfile();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const login = useCallback(async (username, password) => {
    setLoading(true);
    try {
      const data = await apiPost("/auth/login/", { username, password });
      setAuth(data.token, data.user);
      setUser(data.user);
      return { ok: true };
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      if (isAuthenticated()) {
        await apiPost("/auth/logout/", {});
      }
    } catch {
      // ignore network errors on logout
    } finally {
      clearAuth();
      setUser(null);
    }
  }, []);

  const updateUser = useCallback((next) => {
    setUser(next);
    setStoredUser(next);
  }, []);

  const value = {
    user,
    login,
    logout,
    loading,
    updateUser,
    refreshProfile,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return ctx;
}
