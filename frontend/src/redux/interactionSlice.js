import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axios from "axios";

export const fetchInteractions = createAsyncThunk(
  "interaction/fetch",
  async () => {
    const res = await axios.get("http://127.0.0.1:8000/interaction/all");
    return res.data;
  }
);

export const addInteraction = createAsyncThunk(
  "interaction/add",
  async (data) => {
    await axios.post("http://127.0.0.1:8000/interaction/interaction", data);
    return data;
  }
);

const slice = createSlice({
  name: "interaction",
  initialState: { list: [] },
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(fetchInteractions.fulfilled, (state, action) => {
      state.list = action.payload;
    });
  }
});

export default slice.reducer;