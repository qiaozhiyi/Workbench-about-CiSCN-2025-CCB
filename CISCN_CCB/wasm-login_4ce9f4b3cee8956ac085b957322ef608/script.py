import crypto from "node:crypto";

import { authenticate } from "./build/release.js";

const target = "ccaf33e3512e31f3";
const start = new Date("2025-12-21T23:00:00+08:00").getTime();
const end   = new Date("2025-12-22T03:00:00+08:00").getTime();

const obj = JSON.parse(authenticate("admin", "admin"));
const md5 = crypto.createHash("md5").update(JSON.stringify(obj)).digest("hex");
if (md5.startsWith(target)) { console.log("hit", t, obj); break; }}