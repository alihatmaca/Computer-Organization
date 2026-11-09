grup:
        mv      a5,a0
        li      a4,49
        ble     a0,a4,.L3
        li      a4,64
        li      a0,1
        ble     a5,a4,.L1
        li      a4,74
        li      a0,2
        ble     a5,a4,.L1
        li      a0,84
        sgt     a0,a5,a0
        addi    a0,a0,3
        ret
.L3:
        li      a0,0
.L1:
        ret
main:
        addi    sp,sp,-48
        sw      ra,44(sp)
        sw      s0,40(sp)
        sw      s1,36(sp)
        sw      s2,32(sp)
        sw      s3,28(sp)
        sw      s4,24(sp)
        sw      s5,20(sp)
        sw      s6,16(sp)
        sw      s7,12(sp)
        sw      s8,8(sp)
        sw      s9,4(sp)
        lla     s0,.LANCHOR0
        lla     s2,.LANCHOR0+160
        mv      a2,s0
        li      a3,1228800
        addi    a3,a3,1216
        li      a7,1662976
        addi    a7,a7,1549
        li      a6,1013903360
        addi    a6,a6,863
        li      a0,1148157952
        addi    a0,a0,1623
        li      t1,101
.L8:
        mul     a3,a3,a7
        add     a3,a3,a6
        srli    a4,a3,16
        mulhu   a5,a4,a0
        sub     a1,a4,a5
        srli    a1,a1,1
        add     a5,a5,a1
        srli    a5,a5,6
        mul     a5,a5,t1
        sub     a4,a4,a5
        sw      a4,0(a2)
        addi    a2,a2,4
        bne     a2,s2,.L8
        lw      s5,.LANCHOR0+160
        lla     s1,.LANCHOR0
        li      s7,0
        li      s3,0
        mv      s4,s1
        li      s6,55
        li      s8,1
        j       .L10
.L9:
        slli    a0,a0,2
        add     a0,s4,a0
        sw      a5,164(a0)
        addi    s1,s1,4
        beq     s1,s2,.L19
.L10:
        lw      s9,0(s1)
        add     s3,s3,s9
        mv      a0,s9
        call    grup
        slli    a5,a0,2
        add     a5,s4,a5
        lw      a5,164(a5)
        addi    a5,a5,1
        ble     s9,s6,.L9
        addi    s5,s5,1
        mv      s7,s8
        j       .L9
.L19:
        beq     s7,zero,.L11
        sw      s5,.LANCHOR0+160,a5
.L11:
        li      a4,1717985280
        addi    a4,a4,1639
        mulh    a4,s3,a4
        srai    a4,a4,4
        srai    s3,s3,31
        sub     a4,a4,s3
        lla     a5,.LANCHOR0
        sw      a4,184(a5)
        lw      a3,188(a5)
        li      a2,0
        li      a1,1
        j       .L13
.L12:
        addi    s0,s0,4
        beq     s0,s2,.L20
.L13:
        lw      a5,0(s0)
        ble     a4,a5,.L12
        ori     a5,a5,256
        sw      a5,0(s0)
        addi    a3,a3,1
        mv      a2,a1
        j       .L12
.L20:
        beq     a2,zero,.L14
        sw      a3,.LANCHOR0+188,a5
.L14:
        li      a0,0
        lw      ra,44(sp)
        lw      s0,40(sp)
        lw      s1,36(sp)
        lw      s2,32(sp)
        lw      s3,28(sp)
        lw      s4,24(sp)
        lw      s5,20(sp)
        lw      s6,16(sp)
        lw      s7,12(sp)
        lw      s8,8(sp)
        lw      s9,4(sp)
        addi    sp,sp,48
        jr      ra
SID:
        .word   1230016
        .set    .LANCHOR0,. + 0
notlar:
        .zero   160
pass_count:
        .zero   4
bucket:
        .zero   20
mean:
        .zero   4
below_count:
        .zero   4
