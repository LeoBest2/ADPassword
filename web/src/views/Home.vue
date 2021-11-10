<template>
  <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
    <el-form
      ref="loginForm"
      :model="loginForm"
      status-icon
      :rules="rules"
      label-width="120px"
      style="width: 400px;"
    >
      <el-form-item label="域账号" prop="username" placeholder="user" required>
        <el-input v-model="loginForm.username" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="旧密码" prop="oldPwd" required>
        <el-input v-model="loginForm.oldPwd" type="password" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="newPwd" required>
        <el-input v-model="loginForm.newPwd" type="password" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item label="重复密码" prop="repeatNewPwd">
        <el-input v-model="loginForm.repeatNewPwd" type="password" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('loginForm')" style="width: 100%;">登陆</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>

import { ElMessage } from 'element-plus'
export default {
  data() {
    const checkPwd = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('请出入重复新密码'))
      } else if (this.loginForm.newPwd != this.loginForm.repeatNewPwd) {
        return callback(new Error('两次密码需一致'))
      }
      return callback()
    }
    return {
      loginForm: {
        username: '',
        oldPwd: '',
        newPwd: '',
        repeatNewPwd: ''
      },
      checkPwd: checkPwd,
      rules: {
        username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
        oldPwd: [{ required: true, message: '请输入旧密码', trigger: 'blur' }],
        newPwd: [{ required: true, message: '请输入新密码', trigger: 'blur' }],
        repeatNewPwd: [{ validator: checkPwd, trigger: 'blur' }]
      },
    }
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$store.commit('login', this.loginForm.username)
          ElMessage({
            showClose: true,
            message: `用户 ${this.loginForm.username} 登陆成功!`,
            type: 'success',
          })
          this.$router.replace({ name: 'Home' })
        } else {
          return false
        }
      })
    }
  },
  components: {
  }
}
</script>